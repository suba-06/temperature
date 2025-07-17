import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

def estimate_temperature(frame):
    # Convert BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    red_channel = rgb[:, :, 0]
    green_channel = rgb[:, :, 1]
    blue_channel = rgb[:, :, 2]

    # Create a skin-tone mask (very basic)
    mask = (red_channel > 80) & (green_channel > 50) & (blue_channel < 100)

    if np.count_nonzero(mask) == 0:
        return "Unable to detect face area"

    avg_red = np.mean(red_channel[mask])

    # Estimate temp based on red value
    tempC = (avg_red - 50) / 2 + 36
    tempC = max(34, min(40, tempC))  # clamp
    tempF = (tempC * 9/5) + 32

    return f"Estimated Body Temp: {tempC:.1f} °C / {tempF:.1f} °F (Approx)"

def update_frame():
    ret, frame = cap.read()
    if ret:
        # Convert to Tkinter-compatible image
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        video_label.imgtk = img_tk
        video_label.configure(image=img_tk)
    root.after(10, update_frame)

def capture_and_estimate():
    ret, frame = cap.read()
    if ret:
        temp_text = estimate_temperature(frame)
        result_label.config(text=temp_text)

# GUI Setup
root = Tk()
root.title("Body Temperature Estimator")

video_label = Label(root)
video_label.pack(padx=10, pady=10)

scan_button = Button(root, text="Tap to Scan", command=capture_and_estimate, bg="#4caf50", fg="white", font=("Arial", 14))
scan_button.pack(pady=10)

result_label = Label(root, text="Waiting for scan...", font=("Arial", 16))
result_label.pack(pady=10)

# Start webcam
cap = cv2.VideoCapture(0)
update_frame()

root.mainloop()

# Release camera when closing
cap.release()
cv2.destroyAllWindows()
