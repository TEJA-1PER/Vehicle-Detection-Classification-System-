# GUI.py

import tkinter as tk
from tkinter import filedialog, Canvas, Label, Button, PhotoImage
import os
import subprocess
import sys
import threading

# Global handle for the running detection process
proc = None

# --- GUI setup ---
top = tk.Tk()
top.geometry('1200x750')
top.title('Deep CNN Framework for Object Detection and Classification System from Real Time Videos')

# Background image
bg = PhotoImage(file="a.png")
canvas1 = Canvas(top, width=1200, height=750)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")

# Heading
heading = Label(
    top,
    text="Deep CNN Framework for Object Detection and Classification System from Real Time Videos",
    pady=20,
    font=('Arial', 20, 'bold'),
    bg='#CDCDCD',
    fg='#FF0000',
    justify='center'       # center the text inside the Label
)
canvas1.create_window(600, 50, window=heading, anchor='center')

label = Label(top, background='#CDCDCD', font=('Arial', 15, 'bold'))
canvas1.create_window(600, 700, window=label)

# Placeholder for the classify button
top.classify_b = None

# Stop button (disabled until detection is running)
stop_btn = Button(
    top,
    text="Stop Detection",
    state="disabled",
    command=lambda: stop_detection(),
    padx=10, pady=5,
    background='#a83232',
    foreground='white',
    font=('Arial', 10, 'bold')
)
canvas1.create_window(700, 600, window=stop_btn)


def monitor_process():
    global proc
    if proc is not None:
        out, err = proc.communicate()
        if proc.returncode == 0:
            label.config(text="Processing complete!", foreground="green")
        else:
            label.config(text=f"Error:\n{err}", foreground="red")
        proc = None
    else:
        label.config(text="No process was started.", foreground="red")
    top.classify_b.config(state="normal")
    stop_btn.config(state="disabled")


def classify(file_path):
    global proc
    out_dir = os.path.join(os.getcwd(), "outputVideos")
    os.makedirs(out_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(out_dir, f"{base}_out.avi")

    yolo_model = "yolo-"  # adjust based on your directory structure

    cmd = [
        sys.executable,
        os.path.join(os.getcwd(), "Main1.py"),
        "--input", file_path,
        "--output", output_path,
        "--yolo", yolo_model
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        label.config(text="Processing...", foreground="blue")
        top.classify_b.config(state="disabled")
        stop_btn.config(state="normal")

        threading.Thread(target=monitor_process, daemon=True).start()
    except Exception as e:
        label.config(text=f"Failed to start detection:\n{str(e)}", foreground="red")
        proc = None


def stop_detection():
    global proc
    if proc and proc.poll() is None:
        proc.terminate()
        label.config(text="Detection stopped.", foreground="orange")
        top.classify_b.config(state="normal")
        stop_btn.config(state="disabled")
        proc = None


def show_classify_button(file_path):
    if top.classify_b:
        top.classify_b.destroy()

    top.classify_b = Button(
        top,
        text="Get RealTime Reading",
        command=lambda: classify(file_path),
        padx=10, pady=5,
        background='#364156',
        foreground='white',
        font=('Arial', 10, 'bold')
    )
    canvas1.create_window(500, 600, window=top.classify_b)


def upload_video():
    file_path = filedialog.askopenfilename(
        filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv"), ("All files", "*.*")]
    )
    if file_path:
        label.config(text="")  # clear any previous status
        show_classify_button(file_path)


# Upload button
upload = Button(
    top,
    text="Upload Input Video",
    command=upload_video,
    padx=10, pady=5,
    background='#364156',
    foreground='white',
    font=('Arial', 10, 'bold')
)
canvas1.create_window(600, 550, window=upload)

top.mainloop()
