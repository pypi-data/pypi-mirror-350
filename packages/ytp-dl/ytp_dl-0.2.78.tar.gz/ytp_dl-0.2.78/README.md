# ytp-dl · v0.2.78

**ytp-dl** is a headless YouTube downloader that tunnels all traffic through
Mullvad VPN and exposes an optional Flask API.  
It’s packaged for one‑command deployment on a fresh Ubuntu VPS.

---

## Features

* `ytp-dl` — CLI: download a video or audio with one line
* `ytp-dl-api` — Flask server for remote JSON downloads
* Hard‑coded virtual‑env path `/opt/yt-dlp-mullvad/venv` for consistency
* Automatic yt‑dlp, thumbnail, and metadata embedding
* Clear environment validation & helpful error messages

---

## VPS Installation Guide (PyPI workflow)

**Tested on Ubuntu 22.04 DigitalOcean droplets**

```bash
# 1) SSH in
ssh root@<droplet_ip>

# 2) OS prerequisites
sudo apt update && sudo apt install -y python3-venv python3-pip curl ffmpeg

# 3) Mullvad CLI
curl -fsSLo /tmp/mullvad.deb https://mullvad.net/download/app/deb/latest/
sudo apt install -y /tmp/mullvad.deb

# 4) Project directory + venv (must match package expectations)
mkdir -p /opt/yt-dlp-mullvad
python3 -m venv /opt/yt-dlp-mullvad/venv
source /opt/yt-dlp-mullvad/venv/bin/activate

# 5) Install from PyPI
pip install --upgrade pip
pip install ytp-dl==0.2.78
```

### Quick smoke‑test

```bash
ytp-dl "https://youtu.be/dQw4w9WgXcQ" <mullvad_account> --resolution 720
# Expect: DOWNLOADED_FILE:/root/Rick Astley - Never Gonna Give You Up.mp4
```

### Persist the API with systemd

```bash
sudo tee /etc/systemd/system/ytp-dl-api.service > /dev/null <<'EOF'
[Unit]
Description=Flask API for ytp-dl Mullvad Downloader
After=network.target

[Service]
User=root
WorkingDirectory=/opt/yt-dlp-mullvad
Environment=VIRTUAL_ENV=/opt/yt-dlp-mullvad/venv
Environment=PATH=/opt/yt-dlp-mullvad/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
ExecStart=/opt/yt-dlp-mullvad/venv/bin/ytp-dl-api --host 0.0.0.0 --port 5000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now ytp-dl-api
systemctl status ytp-dl-api
```

Once running, download via HTTP:

```bash
curl -X POST http://<droplet_ip>:5000/api/download \
     -H 'Content-Type: application/json' \
     -d '{"url":"https://youtu.be/dQw4w9WgXcQ","mullvad_account":"<acct>"}' \
     -O -J
```

---

## CLI Examples

```bash
# Best quality video (default mp4):
ytp-dl "<url>" <acct>

# Force 1080p WebM:
ytp-dl "<url>" <acct> --resolution 1080 --extension webm

# Extract audio as MP3:
ytp-dl "<url>" <acct> --extension mp3
```

---

## Development & Publishing

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt twine wheel setuptools
python setup.py sdist bdist_wheel
twine upload dist/*
```

---

## License
MIT – © dumgum82 2025
