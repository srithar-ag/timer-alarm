import tkinter as tk
import math
import os

WIDTH = 520
HEIGHT = 560
RADIUS = 180

root = tk.Tk()
root.title("Ultra Modern Alarm Timer")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg="#0b1120")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0b1120", highlightthickness=0)
canvas.pack()

# background circle
canvas.create_oval(
    WIDTH/2-RADIUS, HEIGHT/2-RADIUS,
    WIDTH/2+RADIUS, HEIGHT/2+RADIUS,
    outline="#1f2937",
    width=18
)

timer_text = canvas.create_text(
    WIDTH/2,
    HEIGHT/2,
    text="00:00",
    fill="#22d3ee",
    font=("Helvetica", 52, "bold")
)

arc = None
remaining = 0
total = 0
running = False


def draw_progress():
    global arc

    progress = (total - remaining) / total if total else 0
    angle = progress * 360

    if arc:
        canvas.delete(arc)

    arc = canvas.create_arc(
        WIDTH/2-RADIUS,
        HEIGHT/2-RADIUS,
        WIDTH/2+RADIUS,
        HEIGHT/2+RADIUS,
        start=90,
        extent=-angle,
        outline="#22d3ee",
        width=18,
        style="arc"
    )


def update_timer():
    global remaining, running

    if running and remaining >= 0:
        mins = remaining // 60
        secs = remaining % 60

        canvas.itemconfig(timer_text, text=f"{mins:02d}:{secs:02d}")

        draw_progress()

        remaining -= 1
        root.after(1000, update_timer)

    elif remaining < 0:
        running = False
        os.system("afplay alarm.wav")


def start():
    global remaining, total, running

    if not running:
        m = int(min_entry.get())
        s = int(sec_entry.get())

        total = m * 60 + s
        remaining = total
        running = True

        update_timer()


def pause():
    global running
    running = False


def reset():
    global running, remaining
    running = False
    remaining = 0
    canvas.itemconfig(timer_text, text="00:00")
    if arc:
        canvas.delete(arc)


# title
title = tk.Label(
    root,
    text="⏰ Alarm Timer",
    font=("Helvetica", 26, "bold"),
    fg="white",
    bg="#0b1120"
)
title.place(x=180, y=20)


# input fields
min_entry = tk.Entry(root, width=5, font=("Helvetica", 18), justify="center")
min_entry.place(x=200, y=430)

sec_entry = tk.Entry(root, width=5, font=("Helvetica", 18), justify="center")
sec_entry.place(x=270, y=430)


# buttons
start_btn = tk.Button(root, text="Start", font=("Helvetica", 14), bg="#22d3ee", command=start)
start_btn.place(x=160, y=480)

pause_btn = tk.Button(root, text="Pause", font=("Helvetica", 14), bg="#facc15", command=pause)
pause_btn.place(x=230, y=480)

reset_btn = tk.Button(root, text="Reset", font=("Helvetica", 14), bg="#ef4444", command=reset)
reset_btn.place(x=310, y=480)


root.mainloop()