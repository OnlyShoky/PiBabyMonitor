
# PiBabyMonitor

A simple Raspberry Pi baby monitor system using Flask.  
It streams live video from the Pi camera and supports audio streaming via ffmpeg.  
Designed to run on a Raspberry Pi and accessible from your local network.

---

## Features

- Live video streaming from Raspberry Pi camera (OpenCV)
- Audio streaming via `ffmpeg` (HLS format)
- Easy reset of the camera via a Flask API endpoint
- Runs as a systemd service for automatic startup and easy management

---

## Project Structure

```

camera-project/
├── app.py                # Main Flask app
├── static/
│   ├── hls/              # Folder for audio streaming files (auto-cleaned)
│   └── assets/           # Place your demo.gif here (if used)
├── templates/
│   └── index.html        # Main HTML page
├── requirements.txt      # Python dependencies
└── README.md             # This file

````

---

## Installation & Setup

### 1. Clone the repository on your Raspberry Pi

```bash
git clone https://github.com/yourusername/pibabymonitor.git
cd pibabymonitor
````

### 2. Install Python dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 3. Install system dependencies for ffmpeg and OpenCV (if not installed)

```bash
sudo apt update
sudo apt install ffmpeg python3-opencv
```

### 4. Run the app locally (for testing)

```bash
python3 app.py
```

Then open your browser and navigate to:

```
http://<your-raspberry-pi-ip>:5000
```

---

## Using the Systemd Service (Recommended for production)

To keep the app running automatically on boot and in the background, set up a systemd service:

### Create the systemd service file

```bash
sudo nano /etc/systemd/system/camera-project.service
```

### Paste the following content

```ini
[Unit]
Description=Flask Camera Project
After=network.target

[Service]
User=shoky
WorkingDirectory=/home/shoky/Desktop/Projects/camera-project
ExecStart=/usr/bin/python3 /home/shoky/Desktop/Projects/camera-project/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Enable and start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable camera-project.service
sudo systemctl start camera-project.service
```

### Manage the service

* Check status:

```bash
sudo systemctl status camera-project.service
```

* Stop service:

```bash
sudo systemctl stop camera-project.service
```

* Restart service:

```bash
sudo systemctl restart camera-project.service
```

* Disable autostart:

```bash
sudo systemctl disable camera-project.service
```

---

## Notes

* Verify your Python interpreter path with `which python3` and update the service file if needed.
* If you use a virtual environment or environment variables, adjust the `ExecStart` accordingly.
* The service runs as user `shoky`. Ensure that this user has proper permissions to access the camera and folders.
* The app automatically cleans temporary streaming files on startup.
* Audio streaming runs as an `ffmpeg` subprocess managed by the Flask app.

---

## Troubleshooting

* If the camera feed stops or fails, use the `/reset_camera` endpoint to reset the camera without restarting the whole app.
* Make sure your camera device is correctly configured and accessible by OpenCV (`/dev/video0`).
* Check `journalctl -u camera-project.service` for logs if running as a systemd service.

---

## License

MIT License

---

## Contact

For questions or suggestions, open an issue or contact `your-email@example.com`.

---

Thank you for using PiBabyMonitor! 👶📹

```

---

If you want, I can save it as a file in your environment. Just say the word!
```
