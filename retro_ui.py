import tkinter as tk
from tkinter import ttk
from engine import SceneEngine

BG = "#000000"
FG = "#00FF66"
ACCENT = "#00AA44"
FONT = ("Courier New", 14)
FONT_TITLE = ("Courier New", 18, "bold")
FONT_SMALL = ("Courier New", 10)

class RetroApp:
    def __init__(self, root):
        self.root = root
        self.engine = SceneEngine()

        root.title("NEON PATH v1.0")
        root.configure(bg=BG)

        self.frame = tk.Frame(root, bg=BG)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.title_label = tk.Label(
            self.frame, text="NEON PATH // SYS-LINK INTERFACE",
            fg=FG, bg=BG, font=FONT_TITLE
        )
        self.title_label.pack(anchor="w")

        self.divider = tk.Label(
            self.frame, text="=" * 60,
            fg=ACCENT, bg=BG, font=FONT
        )
        self.divider.pack(anchor="w", pady=(5, 10))

        self.text_area = tk.Label(
            self.frame, text="", fg=FG, bg=BG,
            font=FONT, justify="left"
        )
        self.text_area.pack(anchor="w", fill="both", expand=True)

        self.question_label = tk.Label(
            self.frame, text="", fg=ACCENT, bg=BG,
            font=FONT, justify="left"
        )
        self.question_label.pack(anchor="w", pady=(10, 5))

        btn_frame = tk.Frame(self.frame, bg=BG)
        btn_frame.pack(anchor="w", pady=(5, 10))

        self.yes_btn = tk.Button(
            btn_frame, text="[ YES ]", width=10,
            fg=BG, bg=FG, activebackground=ACCENT,
            activeforeground=BG, font=FONT,
            command=self.on_yes
        )
        self.yes_btn.grid(row=0, column=0, padx=(0, 10))

        self.no_btn = tk.Button(
            btn_frame, text="[  NO ]", width=10,
            fg=BG, bg=FG, activebackground=ACCENT,
            activeforeground=BG, font=FONT,
            command=self.on_no
        )
        self.no_btn.grid(row=0, column=1)

        self.status_label = tk.Label(
            self.frame, text="BOOTING NEON PATH...",
            fg=ACCENT, bg=BG, font=FONT_SMALL
        )
        self.status_label.pack(anchor="w", pady=(10, 0))

    # UI helpers
    def set_visual(self, text): self.text_area.config(text=text)
    def set_question(self, text): self.question_label.config(text=text)
    def set_status(self, text): self.status_label.config(text=text)

    # Scene control
    def goto_scene(self, name):
        scene = self.engine.get(name)
        self.current = scene
        scene.on_show(self)

    def on_yes(self):
        self.set_status("INPUT: YES")
        if self.current.on_answer:
            self.current.on_answer(self, True)

    def on_no(self):
        self.set_status("INPUT: NO")
        if self.current.on_answer:
            self.current.on_answer(self, False)
