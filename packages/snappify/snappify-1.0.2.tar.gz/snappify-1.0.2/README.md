# Snapify

An async CLI to download Snapchat Story media and optionally monitor for new posts. Built by Cass × GPT.

---

## 🚀 Features

- **Async & concurrent** downloads  
- **Single-run** (`snapify -u alice,bob`) or **watch mode** (`snapify start`)  
- **Add/remove** multiple usernames on the fly (`-u`, `-r`)  
- **Configurable poll interval** for automatic checks (`-c`)  
- **Persistent state** in `autopos0.json` to avoid redownloading  
- **ZIP fallback** for large batches  
- **Real-time logging** (via `logging`)  

---

## 📦 Install

```bash
pip install snapify
