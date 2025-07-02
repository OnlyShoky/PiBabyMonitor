from flask import Flask, render_template, Response, jsonify
import cv2
import time
import subprocess
import atexit
import signal

import os
import glob
import shutil


app = Flask(__name__)
camera = cv2.VideoCapture(0)  # Use your camera device

def generate_frames():
    global camera
    while True:
        success, frame = camera.read()
        if not success:
            print("Frame capture failed, reopening camera...")
            camera.release()
            time.sleep(1)  # small delay before reopening
            camera = cv2.VideoCapture(0)
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("Failed to encode frame")
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame',
                    headers={
                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                        'Pragma': 'no-cache',
                        'Expires': '0'
                    })
    

@app.route('/reset_camera', methods=['POST'])
def reset_camera():
    global camera
    try:
        camera.release()
    except Exception as e:
        print("Error releasing camera on reset:", e)
    time.sleep(1)
    camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # Flush frames
    for _ in range(5):
        camera.read()
    return jsonify({"status": "camera reset"})


def start_audio_stream():
    cmd = [
        'ffmpeg',
        '-f', 'alsa',
        '-ac', '1',
        '-ar', '44100',
        '-sample_fmt', 's16',
        '-channels', '1',
        '-i', 'hw:3,0',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-ar', '44100',
        '-f', 'hls',
        '-hls_time', '1',
        '-hls_list_size', '3',
        '-hls_flags', 'delete_segments',
        'static/hls/audio.m3u8'
    ]

    print("🎤 Starting audio stream...")
    process = subprocess.Popen(cmd)
    return process

def clean_static_files():
    
    # Path to your static HLS folder
    folder = "static/hls"
    
    # Remove all files in the folder
    files = glob.glob(os.path.join(folder, "*"))
    for f in files:
        try:
            if os.path.isfile(f) or os.path.islink(f):
                os.unlink(f)
            elif os.path.isdir(f):
                shutil.rmtree(f)
        except Exception as e:
            print(f"Error deleting {f}: {e}")

if __name__ == '__main__':
    
    # Call this function before starting your Flask or audio process
    clean_static_files()
    
    # Start ffmpeg audio streaming subprocess
    audio_process = start_audio_stream()

    # Ensure ffmpeg subprocess is terminated when Flask exits
    def cleanup():
        print("🛑 Stopping audio stream...")
        audio_process.terminate()
        audio_process.wait()

    atexit.register(cleanup)
    signal.signal(signal.SIGINT, lambda sig, frame: cleanup())

    # Start Flask app
    app.run(host='0.0.0.0', port=5000, threaded=True)
