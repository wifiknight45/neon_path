#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

# -------------------------
# Retro style helpers
# -------------------------

BG_COLOR = "#000000"
FG_COLOR = "#00FF66"
ACCENT_COLOR = "#00AA44"
FONT_MAIN = ("Courier New", 14)
FONT_TITLE = ("Courier New", 18, "bold")
FONT_SMALL = ("Courier New", 10)

SCENES = {}

def register_scene(name):
    def deco(fn):
        SCENES[name] = fn
        return fn
    return deco

class RetroApp:
    def __init__(self, root):
        self.root = root
        root.title("NEON PATH v1.0")
        root.configure(bg=BG_COLOR)

        # Main frame
        self.frame = tk.Frame(root, bg=BG_COLOR)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        self.title_label = tk.Label(
            self.frame,
            text="NEON PATH // SYS-LINK INTERFACE",
            fg=FG_COLOR,
            bg=BG_COLOR,
            font=FONT_TITLE
        )
        self.title_label.pack(anchor="w")

        # Divider
        self.divider = tk.Label(
            self.frame,
            text="=" * 60,
            fg=ACCENT_COLOR,
            bg=BG_COLOR,
            font=FONT_MAIN
        )
        self.divider.pack(anchor="w", pady=(5, 10))

        # Visual / text area
        self.text_area = tk.Label(
            self.frame,
            text="",
            fg=FG_COLOR,
            bg=BG_COLOR,
            font=FONT_MAIN,
            justify="left"
        )
        self.text_area.pack(anchor="w", fill="both", expand=True)

        # Question
        self.question_label = tk.Label(
            self.frame,
            text="",
            fg=ACCENT_COLOR,
            bg=BG_COLOR,
            font=FONT_MAIN,
            justify="left"
        )
        self.question_label.pack(anchor="w", pady=(10, 5))

        # Buttons
        btn_frame = tk.Frame(self.frame, bg=BG_COLOR)
        btn_frame.pack(anchor="w", pady=(5, 10))

        self.yes_button = tk.Button(
            btn_frame,
            text="[ YES ]",
            command=self.on_yes,
            fg=BG_COLOR,
            bg=FG_COLOR,
            activebackground=ACCENT_COLOR,
            activeforeground=BG_COLOR,
            font=FONT_MAIN,
            width=10
        )
        self.yes_button.grid(row=0, column=0, padx=(0, 10))

        self.no_button = tk.Button(
            btn_frame,
            text="[  NO ]",
            command=self.on_no,
            fg=BG_COLOR,
            bg=FG_COLOR,
            activebackground=ACCENT_COLOR,
            activeforeground=BG_COLOR,
            font=FONT_MAIN,
            width=10
        )
        self.no_button.grid(row=0, column=1)

        # Status line
        self.status_label = tk.Label(
            self.frame,
            text="BOOTING NEON PATH...",
            fg=ACCENT_COLOR,
            bg=BG_COLOR,
            font=FONT_SMALL,
            justify="left"
        )
        self.status_label.pack(anchor="w", pady=(10, 0))

        self.current_scene = None
        self.last_answer = None

        # Start
        self.goto_scene("boot")

    def set_visual(self, text):
        self.text_area.config(text=text)

    def set_question(self, text):
        self.question_label.config(text=text)

    def set_status(self, text):
        self.status_label.config(text=text)

    def goto_scene(self, name):
        self.current_scene = name
        scene_fn = SCENES.get(name)
        if scene_fn:
            scene_fn(self)
        else:
            self.set_visual(f"[ERROR] UNKNOWN SCENE: {name}")
            self.set_question("")
            self.yes_button.config(state="disabled")
            self.no_button.config(state="disabled")

    def on_yes(self):
        self.last_answer = True
        self.set_status("INPUT: YES")
        self.handle_answer()

    def on_no(self):
        self.last_answer = False
        self.set_status("INPUT: NO")
        self.handle_answer()

    def handle_answer(self):
        # Scene decides what to do with last_answer
        scene_fn = SCENES.get(self.current_scene)
        if scene_fn and hasattr(scene_fn, "on_answer"):
            scene_fn.on_answer(self, self.last_answer)

# -------------------------
# Scenes
# -------------------------

@register_scene("boot")
def scene_boot(app: RetroApp):
    visual = r"""
[SYS-BOOT 1986]
MEM CHECK .... OK
CRT LINK  ..... OK
NEON BUS  ..... OK

YOU ARE JACKED INTO:
   >> NEON PATH NODE-01 <<
"""
    app.set_visual(visual)
    app.set_question("CONNECT TO CORE NODE?")
    app.set_status("AWAITING INPUT: YES/NO")

def boot_on_answer(app: RetroApp, ans: bool):
    if ans:
        app.goto_scene("core_hub")
    else:
        app.goto_scene("idle_exit")

scene_boot.on_answer = boot_on_answer


@register_scene("idle_exit")
def scene_idle_exit(app: RetroApp):
    visual = r"""
[LINK-IDLE]
YOU REMAIN OUTSIDE THE GRID.
THE NEON HUM FADES AWAY.

SESSION TERMINATED.
"""
    app.set_visual(visual)
    app.set_question("RESTART SESSION?")
    app.set_status("SESSION IDLE")

def idle_on_answer(app: RetroApp, ans: bool):
    if ans:
        app.goto_scene("boot")
    else:
        app.set_question("SESSION CLOSED.")
        app.yes_button.config(state="disabled")
        app.no_button.config(state="disabled")
        app.set_status("CONNECTION DROPPED")

scene_idle_exit.on_answer = idle_on_answer


@register_scene("core_hub")
def scene_core_hub(app: RetroApp):
    visual = r"""
[CORE-HUB // NODE-01]
GREEN LINES TRACE ACROSS A VIRTUAL GRID.
TERMINALS FLOAT IN THE DARK.

LEFT:  ARCHIVE MATRIX
RIGHT: SIGNAL LABYRINTH
"""
    app.set_visual(visual)
    app.set_question("ROUTE TO ARCHIVE MATRIX? (NO = SIGNAL LABYRINTH)")
    app.set_status("ROUTING DECISION REQUIRED")

def core_hub_on_answer(app: RetroApp, ans: bool):
    if ans:
        app.goto_scene("archive")
    else:
        app.goto_scene("signals")

scene_core_hub.on_answer = core_hub_on_answer


@register_scene("archive")
def scene_archive(app: RetroApp):
    visual = r"""
[ARCHIVE-MATRIX]
STACKS OF DATA CUBES GLOW FAINTLY.
OLD LOGS, LOST USERS, FORGOTTEN PATHS.

A SINGLE CUBE PULSES BRIGHTER THAN THE REST.
"""
    app.set_visual(visual)
    app.set_question("ACCESS THE PULSING DATA CUBE?")
    app.set_status("ARCHIVE ACCESS STANDBY")

def archive_on_answer(app: RetroApp, ans: bool):
    if ans:
        app.goto_scene("archive_deep")
    else:
        app.goto_scene("core_hub")

scene_archive.on_answer = archive_on_answer


@register_scene("archive_deep")
def scene_archive_deep(app: RetroApp):
    visual = r"""
[ARCHIVE-CORE]
THE CUBE OPENS. INSIDE: A MIRROR OF YOUR OWN SIGNAL.

YOU REALIZE:
   YOU ARE PART OF THE SYSTEM'S MEMORY.

NEON PATH REMEMBERS YOU.
"""
    app.set_visual(visual)
    app.set_question("DISCONNECT FROM ARCHIVE?")
    app.set_status("IDENTITY LOOP DETECTED")

def archive_deep_on_answer(app: RetroApp, ans: bool):
    if ans:
        app.goto_scene("idle_exit")
    else:
        app.set_question("YOU STAY. THE ARCHIVE KEEPS YOU.")
        app.yes_button.config(state="disabled")
        app.no_button.config(state="disabled")
        app.set_status("PERMANENT LINK ESTABLISHED")

scene_archive_deep.on_answer = archive_deep_on_answer


@register_scene("signals")
def scene_signals(app: RetroApp):
    visual = r"""
[SIGNAL-LABYRINTH]
WAVES OF GREEN CODE CASCADE DOWN.
NOISE. ECHOES. FRAGMENTS OF OTHER USERS.

ONE SIGNAL STANDS OUT:
   >> UNKNOWN ORIGIN, HIGH INTENSITY <<
"""
    app.set_visual(visual)
    app.set_question("LOCK ONTO UNKNOWN SIGNAL?")
    app.set_status("SIGNAL ACQUISITION MODE")

def signals_on_answer(app: RetroApp, ans: bool):
    if ans:
        app.goto_scene("signal_lock")
    else:
        app.goto_scene("core_hub")

scene_signals.on_answer = signals_on_answer


@register_scene("signal_lock")
def scene_signal_lock(app: RetroApp):
    visual = r"""
[SIGNAL-LOCK]
THE UNKNOWN SIGNAL RESPONDS.
IT MIRRORS YOUR INPUT, AMPLIFIES YOUR PRESENCE.

FOR A MOMENT, YOU AND THE GRID ARE ONE.
"""
    app.set_visual(visual)
    app.set_question("RELEASE THE SIGNAL?")
    app.set_status("COHERENCE MAXIMUM")

def signal_lock_on_answer(app: RetroApp, ans: bool):
    if ans:
        app.goto_scene("idle_exit")
    else:
        app.set_question("YOU HOLD THE SIGNAL. IT HOLDS YOU.")
        app.yes_button.config(state="disabled")
        app.no_button.config(state="disabled")
        app.set_status("FEEDBACK LOOP ENGAGED")

scene_signal_lock.on_answer = signal_lock_on_answer

# -------------------------
# Main
# -------------------------

def main():
    root = tk.Tk()
    root.geometry("900x500")
    app = RetroApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
