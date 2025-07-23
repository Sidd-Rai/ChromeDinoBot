import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab, Image, ImageTk
import json

# --- CONFIGURABLE ---
PLAYABLE_REGION = (177, 160, 789, 383)  # (left, top, right, bottom)
OUTPUT_FILE = 'scan_box.json'

class ScanBoxSelector:
    def __init__(self, master, img, region):
        self.master = master
        self.region = region
        self.img = img
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas = tk.Canvas(master, width=img.width, height=img.height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        self.rect = None
        self.start_x = self.start_y = self.end_x = self.end_y = None
        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.save_button = tk.Button(master, text="Save", command=self.save_box)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.box = None

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='green', width=2)

    def on_drag(self, event):
        self.end_x = event.x
        self.end_y = event.y
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)
        # Save box in canvas coordinates
        x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
        # Convert to absolute screen coordinates
        abs_x1 = self.region[0] + x1
        abs_y1 = self.region[1] + y1
        abs_x2 = self.region[0] + x2
        abs_y2 = self.region[1] + y2
        self.box = {"left": abs_x1, "top": abs_y1, "right": abs_x2, "bottom": abs_y2}

    def save_box(self):
        if not self.box:
            messagebox.showwarning("No Box", "Please select a region first.")
            return
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(self.box, f)
        messagebox.showinfo("Saved", f"Scan box saved to {OUTPUT_FILE}: {self.box}")


def main():
    # Grab screenshot of playable region
    img = ImageGrab.grab(bbox=PLAYABLE_REGION)
    root = tk.Tk()
    root.title("Adjust Scan Box (Drag to select, then click Save)")
    app = ScanBoxSelector(root, img, PLAYABLE_REGION)
    root.mainloop()

if __name__ == '__main__':
    main() 