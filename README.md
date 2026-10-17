#OSINT-Photo-Hunter# 🕵️ OSINT Photo Hunter

A multi-platform Open Source Intelligence (OSINT) toolkit designed to locate, verify, and analyze an individual's photographs across the public web. 

This tool combines **search engine dorking**, **direct API polling**, **headless browser rendering** (Playwright), **reverse image matching** (TinEye), and **biometric facial recognition** (dlib) to build a comprehensive visual footprint of a target.

## ✨ Features

*   **Multi-Platform Scanning:**
    *   **GitHub & Mastodon:** Direct API polling for high-accuracy profile data.
    *   **Instagram:** Headless browser rendering to bypass JavaScript-heavy UI and extract high-res profile media.
    *   **Pinterest & X/Twitter:** Search engine dorking and public API scraping.
*   **Biometric Verification:**
    *   Uses `face_recognition` (dlib) to compare candidate photos against a reference image.
    *   Filters out false positives (e.g., people with the same name but different faces).
*   **Forensic Metadata Extraction:**
    *   Extracts EXIF data (GPS coordinates, camera model, timestamp) from original images.
*   **Reverse Image Search:**
    *   Integrates with the TinEye API to find where a specific "seed" image has been reposted across the web.
*   **Proxy Rotation:**
    *   Built-in support for proxy pools to evade rate-limiting and IP bans during large-scale scans.

## 🚀 Quick Start

### 1. Prerequisites
*   Python 3.9+
*   C++ Compiler (for `face_recognition`/dlib)
    *   **Linux:** `sudo apt-get install cmake g++`
    *   **macOS:** `brew install cmake`
    *   **Windows:** Ensure Visual Studio Build Tools are installed.

### 2. Installation
```bash
git clone https://github.com/elblaxican/osint-photo-hunter.git
cd osint-photo-hunter

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
