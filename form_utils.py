import tkinter as tk
from datetime import datetime


def validate_vision_distance_input(P):
    if P == "" or P.startswith("20/"):
        return True
    return False

def update_text_input_timestamp(label, label_text, timestamp_var, text_var):
    time = datetime.now().strftime("%H:%M")
    if text_var.get() != "":
        timestamp_var.set(time)
        label.config(text=f"{label_text} @ {time}")
    else: 
        timestamp_var.set(time)
        label.config(text=label_text)

def update_checkbox_timestamp(timestamp_var, checkbox, checkbox_var, checkbox_text): 
    time = datetime.now().strftime("%H:%M")
    if checkbox_var.get(): 
        checkbox.config(text=f"{checkbox_text} @ {time}")
        timestamp_var.set(time)
    else: 
        checkbox.config(text=checkbox_text)
        timestamp_var.set("")

def focus_widget(event):
    widget = event.widget
    widget.focus_set()

def toggle_availability(var, entry, normal_text):
    if var.get() == normal_text: 
        entry.config(state="normal")
    else: 
        entry.config(state="disabled")

def create_row(parent, topic, OD_var, OD_comment_var, OI_var, OI_comment_var, row): 
    OD_option1 = tk.Radiobutton(parent, text="Normal", variable=OD_var, value="Normal")
    OD_option1.grid(row=row, column=0, padx=0, pady=5, sticky="w")
    OD_option2 = tk.Radiobutton(parent, text="Anormal", variable=OD_var, value="Anormal")
    OD_option2.grid(row=row, column=1, padx=10, pady=5, sticky="w")
    OD_comment = tk.Entry(parent, textvariable=OD_comment_var, width=10, state="disabled")
    OD_comment.grid(row=row, column=2, padx=10, pady=5, sticky="w")

    OD_option1.config(command=lambda var=OD_var, entry=OD_comment, normal_text="Anormal": toggle_availability(var, entry, normal_text))
    OD_option2.config(command=lambda var=OD_var, entry=OD_comment, normal_text="Anormal": toggle_availability(var, entry, normal_text))

    tk.Label(parent, text=topic).grid(row=row, column=3, padx=5, pady=2)

    OI_option1 = tk.Radiobutton(parent, text="Normal", variable=OI_var, value="Normal")
    OI_option1.grid(row=row, column=4, padx=0, pady=5, sticky="w")
    OI_option2 = tk.Radiobutton(parent, text="Anormal", variable=OI_var, value="Anormal")
    OI_option2.grid(row=row, column=5, padx=10, pady=5, sticky="w")
    OI_comment = tk.Entry(parent, textvariable=OI_comment_var, width=10, state="disabled")
    OI_comment.grid(row=row, column=6, padx=10, pady=5, sticky="w")

    OI_option1.config(command=lambda var=OI_var, entry=OI_comment, normal_text="Anormal": toggle_availability(var, entry, normal_text))
    OI_option2.config(command=lambda var=OI_var, entry=OI_comment, normal_text="Anormal": toggle_availability(var, entry, normal_text))