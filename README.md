
# 📥 IZU × N4 — Multi-Platform Video Downloader

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Made with](https://img.shields.io/badge/built%20with-HTML%20%7C%20CSS%20%7C%20JavaScript-green)

> A lightweight, mobile-first interface for downloading videos from **YouTube (videos & playlists), Instagram, TikTok, Twitter / X, Facebook, Reddit, Pinterest,** and more.  
> Designed for **ease of use, hacker-style aesthetics**, and straightforward integration with a yt-dlp-powered back-end.

---

## ✨ Key Features

| Feature | Details |
|---------|---------|
| 🔗 **Multi-Platform Support** | Paste a link from any major social platform—one UI handles them all. |
| 🎚️ **Quality Selector** | Choose 4K, 1440 p, 1080 p, “best”, or audio-only for YouTube (videos or playlists). |
| 📱 **Mobile-First Design** | Fully responsive; works great on phones, tablets, and desktops. |
| ⚡ **Snappy UX** | Animated buttons, stateful status messages, and a “thank you” banner on success. |
| 🛠 **Backend-Agnostic** | The HTML/JS front-end can be wired to any REST or IPC service that puts yt-dlp (or similar) behind an API. |
| 🧩 **Pure Vanilla Stack** | No frameworks—just HTML5, CSS3, and plain JavaScript for maximal portability and zero build step. |

---

## 📸 Screenshots

<!-- Replace placeholders with your own screenshots / GIFs -->
| Platform grid | YouTube quality picker |
|---------------|------------------------|
| ![Platform grid](docs/screens/platform-grid.png) | ![Quality picker](docs/screens/quality-picker.png) |

---

## 🚀 Quick Start

1. **Clone** the repository

   ```bash
   git clone https://github.com/izuku6-pixel/video-downloader.git
   cd video-downloader
   ```

2. **Serve** the page (any static server works):

   ```bash
   # Option A – simple Python HTTP server
   python -m http.server 8080
   # Option B – VS Code Live Server extension
   ```

3. **Open** your browser to `http://localhost:8080/mobile_video_downloader.html`.

   > Out-of-the-box the download button is **demo-mode only** and logs the intended request in the console.  
   > Wire it up to your preferred back-end to enable real downloads (see *Integrating a back-end* below).

---

## 🛠️ Integrating a Back-End

| Step | Example |
|------|---------|
| 1. Expose an API endpoint such as `POST /api/download` that accepts `{platform, url, quality}`. | `yt-dlp` in a Docker container is a common choice. |
| 2. Replace the `simulateDownload()` function with `fetch('/api/download', …)` in `mobile_video_downloader.html`. | Lines ~360-400 in the script. |
| 3. Return a signed, time-limited URL or stream for the finished file; update the front-end to start the download. | |

---

## ⚙️ Project Structure

```
.
├── docs/                 # Optional screenshots / diagrams
├── mobile_video_downloader.html
└── README.md             # ← you are here
```

---

## 📄 License

This project is released under the **MIT License**—see `LICENSE` for details.

---

## 🤝 Contributing

1. **Fork** the repo and create your branch: `git checkout -b feature/awesome-thing`
2. **Commit** your changes: `git commit -m 'Add awesome thing'`
3. **Push** and open a **pull request**.
4. Follow the **code style** (plain HTML/CSS/JS) and add screenshots/GIFs when relevant.

---

## 🗺️ Roadmap

- [ ] Drag-and-drop URL detection  
- [ ] Dark-/Light-mode toggle  
- [ ] Progressive-Web-App (PWA) offline shell  
- [ ] Localization (i18n)

---

## 🙏 Acknowledgements

- **yt-dlp** — the powerhouse that makes modern video downloading possible  
- **Font Awesome / Twemoji** for easy emoji icons  
- All early testers who broke things so you don’t have to

---

> **Crafted with ☕ &nbsp;+ 💚 by IZU × N4**
