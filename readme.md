# PiBabyMonitor

A Raspberry Pi baby monitoring system streaming live video and audio over your local network. Built with Flask, OpenCV, and FFmpeg, it supports multiple clients, automatic camera reset, and runs as a systemd service for easy startup.

---

![PiBabyMonitor Demo](assets/demo.gif)


## Features

- Live video streaming with automatic camera recovery  
- Live audio streaming powered by FFmpeg and ALSA  
- Supports multiple simultaneous viewers  
- Runs as a systemd service on Raspberry Pi for automatic startup  
- Simple web interface accessible from any device on your LAN  
- Easy to extend and customize  

---

## Hardware Requirements

- Raspberry Pi (any model with camera support)  
- USB or Pi Camera Module  
- Microphone or audio input device  

---

## Software Requirements

- Raspberry Pi OS (or compatible Linux distro)  
- Python 3  
- OpenCV (`opencv-python`)  
- Flask  
- FFmpeg  
- ALSA utilities  

---

## Installation

1. Clone this repo or copy files to your Raspberry Pi.

2. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
