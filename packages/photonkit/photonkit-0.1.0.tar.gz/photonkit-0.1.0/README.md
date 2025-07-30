# 📸 Photonic

**Photonic** is a mildly opinionated backup tool that helps you copy and organize your photos and videos from memory cards, phones, or cameras into your main storage drive — automatically grouped by date and camera.

It is opinionated in that it assumes and imposes a directory strcture and processing rules. It uses EXIF data in photos to automatically organize the photo and video content.

---

## ✅ What Photonic Does

- Copies your photos/videos into target folders in the following structure:

```

YourTargetStorageDrive/
└── 2025/
  └── 2025-05-24/
    └── canon-eos-r5/
        ├── jpg/
        ├── raw/
        └── video/

```

- Works with:
  - `.jpg`, `.jpeg`, `.heic` (from iPhones)
  - RAW files: `.cr3`, `.cr2`, `.nef`, `.arw`
  - Video: `.mov`, `.mp4`, `.avi`

- Reads the **camera name** and **photo date** automatically.
- Skips hidden or duplicate files safely.

---

## 🚀 How to Run

### 1. Make sure ExifTool is installed (once)

Open Terminal and run:

```bash
brew install exiftool
````

### 2. Run Photonic

Replace the folder paths below with your actual source and target:

```bash
python backup/photo_backup.py \
  --source "/Volumes/SDCARD" \
  --target "/Volumes/PhotoDrive"
```

* `--source`: the folder or memory card where your photos are
* `--target`: your main backup drive
✅ This will skip files that are already backed up — perfect for resuming after a crash or unplug.

To allow Photonic to save multiple versions like IMG_1234.jpg, IMG_1234-1.jpg, etc., run:

```bash
python backup/photo_backup.py \
  --source "/Volumes/SDCARD" \
  --target "/Volumes/PhotoDrive" \
  --skip-dupe false
```


---

## 🔄 You Can Restart Anytime

If something goes wrong or you unplug the drive, just run the same command again with `--skip-dupe`. Photonic will:

* Skip the files it already copied
* Only copy what’s missing

---

## 🧼 Safe by Design

* Doesn't overwrite files
* Keeps your photos in neat folders by **date and camera**
* Works great with both Mac Finder and Lightroom

---

## 🧠 Why Use Photonic?

If you've ever thought:

* "Where did I put that trip folder again?"
* "Why is everything dumped in one place?"
* "I don’t want to lose or overwrite anything!"

Photonic does the organizing for you.

---

## ✨ Coming Soon

* A preview mode (dry-run)
* Logging of what was copied
* Optional desktop app

---

Made with ❤️ for photo wranglers.

```

Let me know if you'd like:
- A separate printable “quick start” card
- An AppleScript shortcut wrapper
- A SwiftUI drag-and-drop GUI for Photonic


## 🪪 License

Photonic is released under the [MIT License](LICENSE).