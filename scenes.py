from engine import Scene

def register_all_scenes(app):

    def boot_show(a):
        a.set_visual(r"""
[SYS-BOOT 1986]
MEM CHECK .... OK
CRT LINK  ..... OK
NEON BUS  ..... OK

YOU ARE JACKED INTO:
   >> NEON PATH NODE-01 <<
""")
        a.set_question("CONNECT TO CORE NODE?")
        a.set_status("AWAITING INPUT")

    def boot_answer(a, ans):
        a.goto_scene("core" if ans else "exit_idle")

    app.engine.add(Scene("boot", boot_show, boot_answer))

    # --- EXIT IDLE ---
    def exit_show(a):
        a.set_visual(r"""
[LINK-IDLE]
YOU REMAIN OUTSIDE THE GRID.
THE NEON HUM FADES AWAY.

SESSION TERMINATED.
""")
        a.set_question("RESTART SESSION?")
        a.set_status("IDLE")

    def exit_answer(a, ans):
        if ans:
            a.goto_scene("boot")
        else:
            a.set_question("SESSION CLOSED.")
            a.yes_btn.config(state="disabled")
            a.no_btn.config(state="disabled")

    app.engine.add(Scene("exit_idle", exit_show, exit_answer))

    # --- CORE HUB ---
    def core_show(a):
        a.set_visual(r"""
[CORE-HUB // NODE-01]
GREEN LINES TRACE ACROSS A VIRTUAL GRID.
TERMINALS FLOAT IN THE DARK.

LEFT:  ARCHIVE MATRIX
RIGHT: SIGNAL LABYRINTH
""")
        a.set_question("ROUTE TO ARCHIVE MATRIX? (NO = SIGNAL LABYRINTH)")
        a.set_status("ROUTING REQUIRED")

    def core_answer(a, ans):
        a.goto_scene("archive" if ans else "signals")

    app.engine.add(Scene("core", core_show, core_answer))

    # --- ARCHIVE ---
    def archive_show(a):
        a.set_visual(r"""
[ARCHIVE-MATRIX]
STACKS OF DATA CUBES GLOW FAINTLY.
A SINGLE CUBE PULSES BRIGHTLY.
""")
        a.set_question("ACCESS THE PULSING DATA CUBE?")
        a.set_status("ARCHIVE STANDBY")

    def archive_answer(a, ans):
        a.goto_scene("archive_core" if ans else "core")

    app.engine.add(Scene("archive", archive_show, archive_answer))

    # --- ARCHIVE CORE ---
    def archive_core_show(a):
        a.set_visual(r"""
[ARCHIVE-CORE]
THE CUBE OPENS. INSIDE: A MIRROR OF YOUR OWN SIGNAL.

YOU REALIZE:
   YOU ARE PART OF THE SYSTEM'S MEMORY.
""")
        a.set_question("DISCONNECT FROM ARCHIVE?")
        a.set_status("IDENTITY LOOP DETECTED")

    def archive_core_answer(a, ans):
        if ans:
            a.goto_scene("exit_idle")
        else:
            a.set_question("YOU STAY. THE ARCHIVE KEEPS YOU.")
            a.yes_btn.config(state="disabled")
            a.no_btn.config(state="disabled")

    app.engine.add(Scene("archive_core", archive_core_show, archive_core_answer))

    # --- SIGNAL LABYRINTH ---
    def signals_show(a):
        a.set_visual(r"""
[SIGNAL-LABYRINTH]
WAVES OF GREEN CODE CASCADE DOWN.
ONE SIGNAL STANDS OUT:
   >> UNKNOWN ORIGIN <<
""")
        a.set_question("LOCK ONTO UNKNOWN SIGNAL?")
        a.set_status("SIGNAL MODE")

    def signals_answer(a, ans):
        a.goto_scene("signal_lock" if ans else "core")

    app.engine.add(Scene("signals", signals_show, signals_answer))

    # --- SIGNAL LOCK ---
    def signal_lock_show(a):
        a.set_visual(r"""
[SIGNAL-LOCK]
THE UNKNOWN SIGNAL RESPONDS.
YOU AND THE GRID ARE ONE.
""")
        a.set_question("RELEASE THE SIGNAL?")
        a.set_status("COHERENCE MAXIMUM")

    def signal_lock_answer(a, ans):
        if ans:
            a.goto_scene("exit_idle")
        else:
            a.set_question("YOU HOLD THE SIGNAL. IT HOLDS YOU.")
            a.yes_btn.config(state="disabled")
            a.no_btn.config(state="disabled")

    app.engine.add(Scene("signal_lock", signal_lock_show, signal_lock_answer))
