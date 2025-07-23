import pyautogui
from PIL import ImageGrab
import numpy as np
import time
import threading
import json
import os
from pynput import keyboard as pynput_keyboard  # Use pynput for key detection

# --- CONFIGURABLE PARAMETERS ---
PLAYABLE_REGION = (177, 160, 789, 383)  # (left, top, right, bottom)
SCAN_BOX_FILE = 'scanBoxCoordinates.json'
DINO_X_OFFSET = 80   # Only used if scan_box.json is missing
SCAN_WIDTH = 40      # Only used if scan_box.json is missing
SCAN_HEIGHT = 30     # Only used if scan_box.json is missing
GROUND_OFFSET = 20   # Only used if scan_box.json is missing
JUMP_COOLDOWN = 0.18
SHIFT_PER_SEC = 1.5  # pixels to shift right per second
MAX_SHIFT = 120      # maximum shift in pixels

def get_scan_box_from_file():
    if os.path.exists(SCAN_BOX_FILE):
        with open(SCAN_BOX_FILE, 'r') as f:
            box = json.load(f)
        print(f"[INFO] Using scan box from {SCAN_BOX_FILE}: {box}")
        return (box['left'], box['top'], box['right'], box['bottom'])
    else:
        print("[INFO] scan_box.json not found, using default scan region.")
        left, top, right, bottom = PLAYABLE_REGION
        scan_left = left + DINO_X_OFFSET
        scan_top = bottom - SCAN_HEIGHT - GROUND_OFFSET
        scan_right = scan_left + SCAN_WIDTH
        scan_bottom = bottom - GROUND_OFFSET
        print(f"[INFO] Default scan box: ({scan_left}, {scan_top}, {scan_right}, {scan_bottom})")
        return (scan_left, scan_top, scan_right, scan_bottom)

def detect_obstacle(scan_img, bg_color, threshold=40, min_pixels=8):
    gray = np.array(scan_img.convert('L'))
    diff = np.abs(gray.astype(int) - int(bg_color))
    obstacle_pixels = np.sum(diff > threshold)
    return obstacle_pixels > min_pixels

def get_background_color(region):
    left, top, right, bottom = region
    sample_box = (left + 10, top + 10, left + 30, top + 30)
    img = ImageGrab.grab(bbox=sample_box)
    arr = np.array(img.convert('L'))
    return int(np.median(arr))

# Wait for user to press spacebar to start
def wait_for_space():
    print("Press SPACE to start the bot...")
    space_pressed = [False]
    def on_press(key):
        if key == pynput_keyboard.Key.space:
            space_pressed[0] = True
            return False  # Stop listener
    with pynput_keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    print("[INFO] Spacebar pressed. Starting bot!")

def main():
    last_jump_time = 0
    scan_box_base = get_scan_box_from_file()
    start_time = time.time()
    print("Press Ctrl+C to stop.")
    time.sleep(2)
    while True:
        elapsed = time.time() - start_time
        shift = min(int(SHIFT_PER_SEC * elapsed), MAX_SHIFT)
        # Shift the scan box to the right
        scan_box = (
            scan_box_base[0] + shift,
            scan_box_base[1],
            scan_box_base[2] + shift,
            scan_box_base[3]
        )
        print(f"[DEBUG] Current scan box: {scan_box} (shift: {shift})", end='\r')
        bg_color = get_background_color(scan_box)
        scan_img = ImageGrab.grab(bbox=scan_box)
        obstacle = detect_obstacle(scan_img, bg_color)
        now = time.time()
        if obstacle and now - last_jump_time > JUMP_COOLDOWN:
            print(f"[ACTION] Jump! Obstacle detected at {time.strftime('%H:%M:%S')}.        ")
            pyautogui.press('space')
            last_jump_time = now
        time.sleep(0.01)

if __name__ == "__main__":
    wait_for_space()
    main() 