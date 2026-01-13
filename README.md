# 🎬 VidSnapAI

VidSnapAI is an AI-powered web application that converts images and text into engaging vertical reels with voice narration. It automates reel creation for platforms like Instagram Reels, YouTube Shorts, and TikTok.

---

## 🚀 Features

-  Upload multiple images
-  AI-generated voice narration from text
-  Automatic vertical (9:16) reel generation
-  Fast processing using FFmpeg
-  Simple web interface
-  Social-media-ready output

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Audio:** gTTS (Google Text-to-Speech)
- **Video Processing:** FFmpeg
- **Frontend:** HTML, CSS , Javascript
- **Concurrency:** ThreadPoolExecutor

---

## ⚙️ How It Works

1. User uploads images and enters text
2. Images are normalized to JPEG
3. `input.txt` is created for FFmpeg image sequencing
4. Text is converted to speech (`audio.mp3`)
5. FFmpeg combines images + audio into a vertical video
6. Output is saved to `static/reels/`
7. Processing runs in the background via `ThreadPoolExecutor`

---

## 🖥️ Requirements

- Python **3.9+**
- FFmpeg installed and available in system PATH

---

## 📦 Python Dependencies

```bash
pip install flask pillow gtts werkzeug

```
---

## 🛠️ FFmpeg Installation

- ### Ubuntu / Debian
```bash
sudo apt install ffmpeg

```
- ### macOS (Homebrew)
```bash
brew install ffmpeg

```
- ### Windows

- Download from: https://ffmpeg.org/download.html
- Add FFmpeg to your system PATH

---

## ▶️ Running the App

Run the Flask application:

```bash
python app.py
```

## 📄 Routes Overview

| Route      | Description |
|-----------|-------------|
| `/`       | Home page with featured reels |
| `/create` | Upload images and description |
| `/gallery`| View all generated videos |

---

## 🎥 Video Settings

- **Resolution:** 1080 × 1920  
- **Frame Rate:** 30 FPS  
- **Codec:** libx264  
- **Audio:** AAC  
- **Image Duration:** 2 seconds per image  
- **Aspect Ratio:** Preserved with black padding  

---

## 🧵 Background Processing

- Uses `ThreadPoolExecutor` (2 workers)  
- Each upload is processed asynchronously  
- `.processed` flag prevents duplicate processing  

---

## ⚠️ Notes & Limitations

- gTTS requires an internet connection  
- Designed for short text descriptions  
- Not intended for high-concurrency production use  
- No authentication (demo / prototype focused)  

---

## 🧠 Future Improvements

- Progress status per video  
- Custom image duration  
- Background music support  
- Caption/subtitle overlay  
- User accounts  
- Queue-based workers (Celery / Redis)  

---

## 📜 License

This project is open-source and free to use.  

