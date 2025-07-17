from flask import Flask
import cv2
import numpy as np

app = Flask(__name__)

def estimate_temperature(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    red_channel = rgb[:, :, 0]
    green_channel = rgb[:, :, 1]
    blue_channel = rgb[:, :, 2]

    mask = (red_channel > 80) & (green_channel > 50) & (blue_channel < 100)
    if np.count_nonzero(mask) == 0:
        return "Unable to detect face area"

    avg_red = np.mean(red_channel[mask])
    tempC = (avg_red - 50) / 2 + 36
    tempC = max(34, min(40, tempC))
    tempF = (tempC * 9/5) + 32

    return f"Estimated Body Temp: {tempC:.1f} °C / {tempF:.1f} °F (Approx)"

@app.route('/scan')
def scan():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return "Camera access failed"
    return estimate_temperature(frame)

if __name__ == '__main__':
    app.run(debug=True)
