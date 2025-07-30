#!/usr/bin/env python3
import argparse
import asyncio
import aiohttp
import aiofiles
import json
import logging
import os
import re
import sys
import zipfile
import random
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
from colorama import Fore, Style, init as colorama_init

# Initialize Colorama
colorama_init(autoreset=True)

AUTOPOSTS_FILE = "autoposts.json"
DEFAULT_INTERVAL = 300    # seconds

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

# —————— Persistence ——————————————————————————————
DEFAULT_DATA = {"usernames": {}, "interval": DEFAULT_INTERVAL}

def save_data(data):
    with open(AUTOPOSTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    if not os.path.exists(AUTOPOSTS_FILE):
        print(Fore.YELLOW + "No state file found; creating new one.")
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()
    try:
        with open(AUTOPOSTS_FILE, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(Fore.RED + f"State file corrupt ({e}); resetting.")
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()

    changed = False
    if not isinstance(data.get("usernames"), dict):
        data["usernames"] = {}
        changed = True
    if not isinstance(data.get("interval"), int):
        data["interval"] = DEFAULT_INTERVAL
        changed = True
    if changed:
        print(Fore.YELLOW + "Fixing state file structure.")
        save_data(data)
    return data

# —————— Utility for slugifying titles ——————————————————
def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text

# —————— Extracting media URLs for highlights/spotlights ——————————————————
def extract_media_urls(data):
    """
    Recursively collect every snapList under props.pageProps,
    keyed by its storyTitle.value (if present), else title/displayName,
    else the parent key.
    """
    media = {}
    page_props = data.get("props", {}).get("pageProps", {})

    def recurse(obj, path):
        if isinstance(obj, dict):
            for key, val in obj.items():
                if key == "snapList" and isinstance(val, list):
                    title = (
                        (obj.get("storyTitle") or {}).get("value")
                        or obj.get("title")
                        or obj.get("displayName")
                        or (path[-1] if path else "unknown")
                    )
                    urls = [
                        snap.get("snapUrls", {}).get("mediaUrl")
                        for snap in val
                        if snap.get("snapUrls", {}).get("mediaUrl")
                    ]
                    media.setdefault(title, []).extend(urls)
                else:
                    recurse(val, path + [key])
        elif isinstance(obj, list):
            for item in obj:
                recurse(item, path)

    recurse(page_props, [])
    for album, urls in media.items():
        logging.debug(f"[extract_media_urls] album='{album}' → {len(urls)} URLs")
    return media

# —————— Snapchat Fetching Helpers —————————————————————
async def get_json(session, username):
    url = f"https://story.snapchat.com/@{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    async with session.get(url, headers=headers) as resp:
        if resp.status == 404:
            print(Fore.YELLOW + f"{username}: no story page (404).")
            return None
        text = await resp.text()
        tag = BeautifulSoup(text, "html.parser").find(id="__NEXT_DATA__")
        if not tag:
            print(Fore.RED + f"{username}: no __NEXT_DATA__ found.")
            return None
        try:
            return json.loads(tag.string.strip())
        except Exception as e:
            print(Fore.RED + f"{username}: JSON parse error: {e}")
            return None

# —————— Download a single media URL to a specific directory ——————————————————
async def download_media_to_dir(session, url, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)

    # Parse URL path to get a safe filename, stripping query parameters
    parsed = urlparse(url)
    name = unquote(os.path.basename(parsed.path))
    # Sanitize file name to remove any leftover invalid characters
    name = re.sub(r'[<>:"/\\|?*]', "", name)

    async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
        if resp.status != 200:
            logging.error(f"Failed to download {url}: HTTP {resp.status}")
            return None
        ct = resp.headers.get("Content-Type", "")
        ext = ".jpg" if "image" in ct else ".mp4" if "video" in ct else ""
        if not ext:
            return None

        path = os.path.join(dest_dir, f"{name}{ext}")
        async with aiofiles.open(path, "wb") as f:
            async for chunk in resp.content.iter_chunked(1024):
                await f.write(chunk)
        return path

# —————— ZIP creation ———————————————————————————
async def create_zip(username, files):
    zdir = os.path.join("zips", username)
    os.makedirs(zdir, exist_ok=True)
    zname = f"{username}_{datetime.now():%Y-%m-%d_%H%M}.zip"
    zpath = os.path.join(zdir, zname)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, os.path.basename(f))
    return zpath

# —————— Core Processing (stories + highlights + spotlights) —————————————————
async def process_username(username, session, data, force_zip=False):
    cfg = data["usernames"].setdefault(username, {"last": []})
    last = set(cfg["last"])

    raw = await get_json(session, username)
    if not raw:
        return

    page_props = raw.get("props", {}).get("pageProps", {})
    story = page_props.get("story") or {}
    snaps = story.get("snapList", [])
    story_urls = [s.get("snapUrls", {}).get("mediaUrl") for s in snaps if s.get("snapUrls", {}).get("mediaUrl")]
    new_story = [u for u in story_urls if u not in last]
    story_files = []
    if new_story:
        print(Fore.GREEN + f"{username}: found {len(new_story)} new story item(s), downloading…")
        story_tasks = [
            download_media_to_dir(session, u, os.path.join("snap_media", username, "stories"))
            for u in new_story
        ]
        results_story = await asyncio.gather(*story_tasks)
        story_files = [p for p in results_story if p]
        if story_files:
            if force_zip:
                z = await create_zip(username, story_files)
                for f in story_files:
                    try: os.remove(f)
                    except: pass
                print(Fore.MAGENTA + f"{username}: downloaded {len(story_files)} story snaps (zipped → {z})")
            else:
                print(Fore.MAGENTA + f"{username}: downloaded {len(story_files)} story snaps")
        else:
            print(Fore.RED + f"{username}: story downloads failed.")
        last.update(new_story)
    else:
        print(Fore.CYAN + f"{username}: no new story snaps.")

    media_map = extract_media_urls(raw)

    # — Spotlights (parallelized with gather) —
    spotlight_urls = [
        url for key, lst in media_map.items()
        if "spotlight" in key.lower()
        for url in lst
    ]
    new_spot = [u for u in spotlight_urls if u not in last]
    spot_files = []
    if new_spot:
        print(Fore.GREEN + f"{username}: found {len(new_spot)} new spotlight item(s), downloading…")
        dest_spot = os.path.join("snap_media", username, "spotlights")
        spot_tasks = [
            download_media_to_dir(session, u, dest_spot)
            for u in new_spot
        ]
        results_spot = await asyncio.gather(*spot_tasks)
        spot_files = [p for p in results_spot if p]
        if spot_files:
            if force_zip:
                z_spot = await create_zip(username, spot_files)
                for f in spot_files:
                    try: os.remove(f)
                    except: pass
                print(Fore.MAGENTA + f"{username}: downloaded {len(spot_files)} spotlight snaps (zipped → {z_spot})")
            else:
                print(Fore.MAGENTA + f"{username}: downloaded {len(spot_files)} spotlight snaps")
        else:
            print(Fore.RED + f"{username}: spotlight downloads failed.")
        last.update(new_spot)
    else:
        print(Fore.CYAN + f"{username}: no new spotlight snaps.")

    # — Highlights (parallelized with gather) —
    highlight_keys = sorted([k for k in media_map.keys() if "spotlight" not in k.lower()], key=lambda s: s.lower())
    highlight_pairs = [
        (album_title, u)
        for album_title in highlight_keys
        for u in media_map.get(album_title, [])
    ]
    new_high_pairs = [(t, u) for (t, u) in highlight_pairs if u not in last]
    high_files = []
    if new_high_pairs:
        print(Fore.GREEN + f"{username}: found {len(new_high_pairs)} new highlight item(s), downloading…")
        high_tasks = []
        for album_title, u in new_high_pairs:
            slug = slugify(album_title)
            dest_high = os.path.join("snap_media", username, "highlights", slug)
            high_tasks.append(download_media_to_dir(session, u, dest_high))

        results_high = await asyncio.gather(*high_tasks)
        high_files = [p for p in results_high if p]
        if high_files:
            if force_zip:
                z_high = await create_zip(username, high_files)
                for f in high_files:
                    try: os.remove(f)
                    except: pass
                print(Fore.MAGENTA + f"{username}: downloaded {len(high_files)} highlight snaps (zipped → {z_high})")
            else:
                print(Fore.MAGENTA + f"{username}: downloaded {len(high_files)} highlight snaps")
        else:
            print(Fore.RED + f"{username}: highlight downloads failed.")
        last.update([u for (_, u) in new_high_pairs])
    else:
        print(Fore.CYAN + f"{username}: no new highlight snaps.")

    # Persist the updated 'last' set
    cfg["last"] = list(last)
    save_data(data)

# —————— Highlights-Only Download Helper (parallelized) ———————————————————————————
async def download_highlights_only(username, session, data, force_zip=False):
    cfg = data["usernames"].setdefault(username, {"last": []})
    last = set(cfg["last"])

    raw = await get_json(session, username)
    if not raw:
        return

    media_map = extract_media_urls(raw)
    highlight_keys = sorted([k for k in media_map.keys() if "spotlight" not in k.lower()], key=lambda s: s.lower())
    highlight_pairs = [
        (album_title, u)
        for album_title in highlight_keys
        for u in media_map.get(album_title, [])
    ]
    new_high_pairs = [(t, u) for (t, u) in highlight_pairs if u not in last]
    if not new_high_pairs:
        print(Fore.CYAN + f"{username}: no new highlight snaps.")
        return

    print(Fore.GREEN + f"{username}: found {len(new_high_pairs)} new highlight item(s), downloading…")
    high_tasks = []
    for album_title, u in new_high_pairs:
        slug = slugify(album_title)
        dest_high = os.path.join("snap_media", username, "highlights", slug)
        high_tasks.append(download_media_to_dir(session, u, dest_high))

    results_high = await asyncio.gather(*high_tasks)
    high_files = [p for p in results_high if p]

    if not high_files:
        print(Fore.RED + f"{username}: highlight downloads failed.")
        return

    if force_zip:
        z_high = await create_zip(username, high_files)
        for f in high_files:
            try: os.remove(f)
            except: pass
        print(Fore.MAGENTA + f"{username}: downloaded {len(high_files)} highlight snaps (zipped → {z_high})")
    else:
        print(Fore.MAGENTA + f"{username}: downloaded {len(high_files)} highlight snaps")

    last.update([u for (_, u) in new_high_pairs])
    cfg["last"] = list(last)
    save_data(data)

# —————— Spotlights-Only Download Helper (parallelized) —————————————————————————————
async def download_spotlights_only(username, session, data, force_zip=False):
    cfg = data["usernames"].setdefault(username, {"last": []})
    last = set(cfg["last"])

    raw = await get_json(session, username)
    if not raw:
        return

    media_map = extract_media_urls(raw)
    spotlight_urls = [
        url for key, lst in media_map.items()
        if "spotlight" in key.lower()
        for url in lst
    ]
    new_spot = [u for u in spotlight_urls if u not in last]
    if not new_spot:
        print(Fore.CYAN + f"{username}: no new spotlight snaps.")
        return

    print(Fore.GREEN + f"{username}: found {len(new_spot)} new spotlight item(s), downloading…")
    dest_spot = os.path.join("snap_media", username, "spotlights")
    spot_tasks = [
        download_media_to_dir(session, u, dest_spot)
        for u in new_spot
    ]
    results_spot = await asyncio.gather(*spot_tasks)
    spot_files = [p for p in results_spot if p]

    if not spot_files:
        print(Fore.RED + f"{username}: spotlight downloads failed.")
        return

    if force_zip:
        z_spot = await create_zip(username, spot_files)
        for f in spot_files:
            try: os.remove(f)
            except: pass
        print(Fore.MAGENTA + f"{username}: downloaded {len(spot_files)} spotlight snaps (zipped → {z_spot})")
    else:
        print(Fore.MAGENTA + f"{username}: downloaded {len(spot_files)} spotlight snaps")

    last.update(new_spot)
    cfg["last"] = list(last)
    save_data(data)

# —————— Monitoring Loops ———————————————————————————
async def check_loop_all(data, force_zip=False):
    interval = data["interval"]
    async with aiohttp.ClientSession() as session:
        while True:
            for user in list(data["usernames"].keys()):
                await process_username(user, session, data, force_zip=force_zip)
            print(Fore.YELLOW + f"Sleeping {interval}s…")
            await asyncio.sleep(interval)

async def check_loop_highlights(data, force_zip=False):
    interval = data["interval"]
    async with aiohttp.ClientSession() as session:
        while True:
            for user in list(data["usernames"].keys()):
                await download_highlights_only(user, session, data, force_zip=force_zip)
            print(Fore.YELLOW + f"Sleeping {interval}s…")
            await asyncio.sleep(interval)

async def check_loop_spotlights(data, force_zip=False):
    interval = data["interval"]
    async with aiohttp.ClientSession() as session:
        while True:
            for user in list(data["usernames"].keys()):
                await download_spotlights_only(user, session, data, force_zip=force_zip)
            print(Fore.YELLOW + f"Sleeping {interval}s…")
            await asyncio.sleep(interval)

# —————— CLI —————————————————————————————————————
def main():
    parser = argparse.ArgumentParser(
        prog="snapify",
        description="Download Snapchat story media, highlights, and spotlights, or monitor for new snaps"
    )
    parser.add_argument(
        "-u", "--user",
        help="comma-separated usernames to ADD (downloads now)"
    )
    parser.add_argument(
        "-r", "--remove",
        help="comma-separated usernames to REMOVE"
    )
    parser.add_argument(
        "-c", "--check-interval", type=int,
        help="set polling interval in seconds"
    )
    parser.add_argument(
        "-z", "--zip", action="store_true",
        help="bundle downloaded snaps into a ZIP"
    )
    parser.add_argument(
        "--highlights", "-hl", action="store_true",
        help="download only highlights for added users"
    )
    parser.add_argument(
        "-s", "--spotlights", action="store_true",
        help="download only spotlights for added users"
    )
    parser.add_argument(
        "command", nargs="?", choices=("start",),
        help="‘start’ to begin monitoring loop"
    )
    args = parser.parse_args()

    data = load_data()
    changed = False
    added = []

    # Add users
    if args.user:
        for u in args.user.split(","):
            u = u.strip()
            if u and u not in data["usernames"]:
                data["usernames"][u] = {"last": []}
                added.append(u)
                print(Fore.GREEN + f"Added user: {u}")
        changed = True

    # Remove users
    if args.remove:
        for u in args.remove.split(","):
            u = u.strip()
            if u in data["usernames"]:
                del data["usernames"][u]
                print(Fore.RED + f"Removed user: {u}")
        changed = True

    # Set interval
    if args.check_interval is not None:
        data["interval"] = args.check_interval
        print(Fore.YELLOW + f"Set interval = {args.check_interval}s")
        changed = True

    # on config change without “start”: save & one-off
    if changed and args.command != "start":
        save_data(data)
        if added:
            async def oneoff():
                async with aiohttp.ClientSession() as session:
                    if args.spotlights:
                        for u in added:
                            await download_spotlights_only(u, session, data, force_zip=args.zip)
                    elif args.highlights:
                        for u in added:
                            await download_highlights_only(u, session, data, force_zip=args.zip)
                    else:
                        for u in added:
                            await process_username(u, session, data, force_zip=args.zip)
            asyncio.run(oneoff())

        print(Style.BRIGHT + "\nTo start monitoring for new snaps, run:")
        zip_flag = " -z" if args.zip else ""
        mode_flag = ""
        if args.spotlights:
            mode_flag = " -s"
        elif args.highlights:
            mode_flag = " -hl"
        print(Fore.CYAN + f"  snapify start{mode_flag}{zip_flag}\n")
        sys.exit(0)

    # Start monitoring loop
    if args.command == "start":
        print(Style.BRIGHT + "Entering watch mode—press Ctrl+C to exit.\n")
        try:
            if args.spotlights:
                asyncio.run(check_loop_spotlights(data, force_zip=args.zip))
            elif args.highlights:
                asyncio.run(check_loop_highlights(data, force_zip=args.zip))
            else:
                asyncio.run(check_loop_all(data, force_zip=args.zip))
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nInterrupted; exiting.")
            save_data(data)
            sys.exit(0)

    parser.print_help()

if __name__ == "__main__":
    main()