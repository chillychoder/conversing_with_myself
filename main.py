import tkinter as tk
import soundfile as sf
import sounddevice as sd
import os
import math

def play_sound(path, device_index):
    data, samplerate = sf.read(path)
    sd.play(data, samplerate, device=device_index)

# INDEX 13 Voicemeeter Input
# INDEX 61 for Mixer to Discord mic

INPUT_INDEX = 13
MIXER_OUT_INDEX = 61

sound_folder = "sounds"
sounds = []

for filename in os.listdir(sound_folder):
    if filename.lower().endswith((".wav", ".mp3", ".ogg")):
        sounds.append(os.path.join(sound_folder, filename))

root = tk.Tk()
root.title("Soundboard")
root.config(bg = "skyblue")

mainframe = tk.Frame(root, width = 500, height = 500)
mainframe.pack(padx = 10, pady = 10, fill = "both")

headerText = tk.Label(mainframe, text= "Soundboard", font = ("Arial", 18, "bold"))
headerText.pack(side="top")

btnCanvas = tk.Canvas(mainframe, highlightthickness=0)

scrollbar = tk.Scrollbar(mainframe, orient= "vertical", command=btnCanvas.yview)
btnCanvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
btnCanvas.pack(side="left", fill="both", expand=True)

btn_grid_frame = tk.Frame(btnCanvas)
canvas_frame_id = btnCanvas.create_window((0, 0), window=btn_grid_frame, anchor="nw")

def on_frame_config(event):
    btnCanvas.configure(scrollregion= btnCanvas.bbox("all"))
btn_grid_frame.bind("<Configure>", on_frame_config)

def on_canvas_config(event):
    btnCanvas.itemconfig(canvas_frame_id, width = event.width)
btnCanvas.bind("<Configure>", on_canvas_config)

def on_mousewheel(event):
    if (event.num == 5 or event.delta < 0):
        btnCanvas.yview_scroll(1, "units")
    elif event.num == 4 or event.delta > 0:
        btnCanvas.yview_scroll(-1, "units")
    else:
        # Windows/macOS fallback
        btnCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
btnCanvas.bind_all("<MouseWheel>", on_mousewheel) # Windows / macOS
btnCanvas.bind_all("<Button-4>", on_mousewheel)   # Linux scroll up
btnCanvas.bind_all("<Button-5>", on_mousewheel)   # Linux scroll down

col_cnt = 5
total_sounds = len(sounds)
row_cnt = math.ceil(total_sounds / col_cnt)

for col in range(col_cnt):
    btn_grid_frame.columnconfigure(col, weight=1)

for idx, filepath in enumerate(sounds):
    row = idx // col_cnt
    col = idx % col_cnt

    display_name = os.path.splitext(os.path.basename(filepath))[0]
    MAX_LEN = 12
    if len(display_name) > MAX_LEN:
        display_name= display_name[MAX_LEN] + "..."
    btn = tk.Button(
        btn_grid_frame, 
        text=display_name,
        width=12,
        height=6,
        wraplength=80, 
        command=lambda path=filepath: [play_sound(path, INPUT_INDEX), play_sound(path, MIXER_OUT_INDEX)])
    btn.grid(row=row, column=col, sticky= "nsew", padx=3, pady=3) 
if total_sounds == 0:
    no_sound_lbl = tk.Label(btn_grid_frame, text= "No sounds", fg="grey")
    no_sound_lbl.pack(pady=20)

root.mainloop()