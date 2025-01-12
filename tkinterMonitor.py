#!/usr/bin/env python3
import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO
import time
import tkinter as tk
import logging
import argparse

#---------- enabling and disabling debug logs ---------------------------------
parser = argparse.ArgumentParser()

parser.add_argument('-v', '--Verbose', action='store_true')

arguments = parser.parse_args()

if arguments.Verbose:
    logging.basicConfig(format="%(levelname)s:%(asctime)s.%(msecs)03d: %(message)s", 
                        level=logging.DEBUG, datefmt="%H:%M:%S", force=True)
else:
    logging.disable()

#----------- source url -------------------------------------------------------
url = 'https://www-sk.icrr.u-tokyo.ac.jp/realtimemonitor/skev.gif'

#---------- function for refreshing images on canvas --------------------------
def refresh_image(canvas, img, image_id):
    response = requests.get(url)

    if response.status_code == 200:
        pil_img = Image.open(BytesIO(response.content))
        img = ImageTk.PhotoImage(pil_img)
        canvas.itemconfigure(image_id, image=img)
    else:
        logging.error(f"""response.status_code ins't 200, response.status_code 
        acctually is {response.status_code}""")
    # repeat every five seconds
    canvas.after(5000, refresh_image, canvas, img, image_id)  

#---------- make root window --------------------------------------------------
root = tk.Tk()
root.configure(background='black')
root.resizable(False, False)
root.title('Super-Kamiokande python realtime monitor')
root.overrideredirect(True)

#---------- make canvas for images --------------------------------------------
canvas = tk.Canvas(root, height=999, width=1057)
img = None  # initially only need a canvas image place-holder
image_id = canvas.create_image(1057/2, 999/2, image=img)
canvas.pack()

#---------- make the whole window movable -------------------------------------
def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def on_move(event):
    x = root.winfo_x() - root.x + event.x
    y = root.winfo_y() - root.y + event.y
    root.geometry(f"+{x}+{y}")

def close_window(event):
    root.destroy()

canvas.bind("<Button-1>", start_move)
canvas.bind("<ButtonRelease-1>", stop_move)
canvas.bind("<B1-Motion>", on_move)
canvas.bind("<Double-1>", close_window)

#---------- start image refreshing and rendering of the whole window ----------
refresh_image(canvas, img, image_id)
root.mainloop()
