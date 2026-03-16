# TitanEncode — HDR Video Mastering Suite

> **Professional HDR video encoding with automatic hardware detection — no configuration needed.**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-GPL%20v3-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey?style=flat-square)
![FFmpeg](https://img.shields.io/badge/Powered%20by-FFmpeg-red?style=flat-square)

---

## What is TitanEncode?

TitanEncode is a graphical interface for encoding video in HDR10 format using FFmpeg and x265. It is designed for anyone who wants professional quality results without having to memorize complex command-line parameters.

**The main advantage:** TitanEncode automatically detects the hardware of your system at startup — CPU cores, AMD/Intel/NVIDIA GPU — and configures itself accordingly. You install it, open it, and it is already ready to work optimally on your machine, whether it is a Raspberry Pi or a workstation with an NVIDIA RTX.

---

## Key Features

### 🔍 Automatic hardware detection
- Detects available CPU threads and sets the optimal default automatically
- Detects GPU encoder: **AMD/Intel VAAPI**, **NVIDIA NVENC**, **Intel QuickSync**
- Shows only the encoders actually available on your system — no options that don't work
- Works on any hardware without touching a single setting

### 🎬 Professional HDR10 support
- Automatically reads **master-display** and **max-cll** metadata from the source file
- Inserts HDR10 metadata correctly in the output via x265
- Your TV will see the same HDR information as the original Blu-ray

### 🎛️ Complete video filters
- **Auto-crop** — detects and removes black bars automatically (analyzes 500 frames)
- **Deband** — removes banding artifacts, optimized for 10-bit HDR
- **Denoise** — hqdn3d for speed, NL-Means for maximum quality
- **Sharpen** — unsharp mask for fine detail enhancement
- **De-interlace** — YADIF for interlaced sources (TV recordings, DVDs)
- **Scale** — resize with lanczos, bicubic, bilinear algorithms

### 🔊 Smart audio/subtitle management
- Lists all audio and subtitle tracks with language and codec
- Automatically reads **default** and **forced** flags from the source
- Choose for each track: Keep / Convert (E-AC3, AAC) / Remove
- Supports multiple audio tracks with independent settings

### 🌍 Multilingual interface
Available in: **Italiano · English · Français · Deutsch · Español**  
Change language at any time from Options → Language menu.

### 📊 Real-time progress
- Progress bar with **ETA** (estimated time remaining)
- Frame counter, encoding speed and elapsed time
- Detailed system log for advanced diagnostics

---

## Requirements

| Software | Minimum version | Install on Arch/CachyOS |
|----------|----------------|------------------------|
| Python | 3.10+ | already installed |
| PyQt6 | 6.4+ | `pip install PyQt6` |
| FFmpeg | 5.0+ | `sudo pacman -S ffmpeg` |
| ffprobe | 5.0+ | included with ffmpeg |

**Optional (for hardware encoding):**

| Software | For what | Install |
|----------|---------|---------|
| mesa-va-drivers | VAAPI — AMD/Intel GPU | `sudo pacman -S mesa` |
| nvidia-utils | NVENC — NVIDIA GPU | `sudo pacman -S nvidia-utils` |

> **Note:** Hardware encoders (VAAPI, NVENC) are much faster than software x265 but produce slightly larger files at equal visual quality. For archival use, libx265 software is recommended.

---

## Installation

### Quick install (Arch / CachyOS / Manjaro)

```bash
# 1. Install dependencies
sudo pacman -S ffmpeg python-pyqt6

# 2. Clone the repository
git clone https://github.com/batmaxino/TitanEncode.git
cd TitanEncode

# 3. Run the install script
bash install.sh
```

The install script:
- Copies the files to `~/TitanEncode/`
- Installs the icon
- Creates the entry in the **Multimedia** section of the application menu
- Updates the KDE/GNOME icon cache

### Manual launch (any Linux / Windows / macOS)

```bash
python3 TitanEncode.py
```

---

## How to use

1. **Load a film** — click LOAD FILM and choose your file (MKV, MP4, TS, AVI, M2TS)
2. **Check video settings** — encoder, quality RF and preset are already optimized for your hardware
3. **Audio tracks** — choose Keep / Convert / Remove for each track
4. **Output folder** — by default saves next to the source, or choose a different folder
5. **Start** — click START ENCODING and monitor progress in the bar

> For maximum archive quality: **libx265 + RF 20 + preset slow**  
> For fast daily conversions: **libx265 + RF 22 + preset medium**

---

## Supported encoders

| Encoder | Type | Quality | Speed | Notes |
|---------|------|---------|-------|-------|
| libx265 | Software CPU | ⭐⭐⭐⭐⭐ | ⭐⭐ | Best for HDR archive |
| libx264 | Software CPU | ⭐⭐⭐⭐ | ⭐⭐⭐ | Maximum compatibility |
| hevc_vaapi | Hardware AMD/Intel | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Fast, requires Mesa |
| hevc_nvenc | Hardware NVIDIA | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Fast, requires nvidia-utils |

---

## Why TitanEncode?

Most video encoding tools either require complex command-line knowledge (FFmpeg, HandBrake CLI) or do not properly support HDR10 metadata (many GUI tools ignore master-display and max-cll, causing incorrect tone mapping on HDR TVs).

TitanEncode bridges this gap:
- **No command line needed** — everything is in the graphical interface
- **HDR10 done right** — metadata is read from the source and written correctly in the output
- **Adapts to your hardware** — detects what your system has and uses it optimally
- **Transparent** — shows the exact FFmpeg command it builds in the log, so advanced users can learn and verify

---

## License

TitanEncode is free and open source software released under the **GNU General Public License v3.0**.

You are free to use, modify and distribute it. See the [LICENSE](LICENSE) file for details.

---

## Support the project

If TitanEncode saved you time and you want to say thanks:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-Ko--fi-FF5E5B?style=flat-square&logo=ko-fi)](https://ko-fi.com/batmaxino)

It is completely optional — the software will always be free. ☕

---

## Contributing

Pull requests are welcome. If you find a bug or want to suggest a feature, open an Issue on GitHub.

---

*TitanEncode — because good video deserves good tools.*
