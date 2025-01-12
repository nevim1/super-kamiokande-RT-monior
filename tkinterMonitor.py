#!/usr/bin/env python3
#------------------------------------------------------------------------------
# Note: 
#   It's important that this code *not* interact directly with tkinter 
#   stuff in the main process since it doesn't support multi-threading.
import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO
import time
import tkinter as tk
import logging
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--Verbose', action='store_true')

arguments = parser.parse_args()

if arguments.Verbose:
    logging.basicConfig(format="%(levelname)s:%(asctime)s.%(msecs)03d: %(message)s", level=logging.DEBUG, datefmt="%H:%M:%S", force=True)
else:
    logging.disable()

url = 'https://www-sk.icrr.u-tokyo.ac.jp/realtimemonitor/skev.gif'

def refresh_image(canvas, img, image_id):
    response = requests.get(url)

    if response.status_code == 200:
        pil_img = Image.open(BytesIO(response.content))
        img = ImageTk.PhotoImage(pil_img)
        canvas.itemconfigure(image_id, image=img)
    else:
        logging.error(f"response.status_code ins't 200, response.status_code acctually is {response.status_code}")
    # repeat every five seconds
    canvas.after(5000, refresh_image, canvas, img, image_id)  


root = tk.Tk()
root.configure(background='black')
root.resizable(False, False)
root.title('Super-Kamiokande python realtime monitor')

canvas = tk.Canvas(root, height=999, width=1057)
img = None  # initially only need a canvas image place-holder
image_id = canvas.create_image(1057/2, 999/2, image=img)
canvas.pack()

refresh_image(canvas, img, image_id)
root.mainloop()
