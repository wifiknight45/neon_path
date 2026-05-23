#!/usr/bin/env python3

from retro_ui import RetroApp
from scenes import register_all_scenes
import tkinter as tk

def main():
    root = tk.Tk()
    root.geometry("900x500")
    app = RetroApp(root)

    register_all_scenes(app)

    app.goto_scene("boot")
    root.mainloop()

if __name__ == "__main__":
    main()
