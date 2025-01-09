import tkinter as tk
from datetime import datetime
from tkinter import font
import form


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
        entry.delete(0, tk.END)
        entry.config(state="disabled")

def create_row(parent, topic, OD_var, OI_var, OD_comment, OI_comment, row, status="normal"): 
    OD_option1 = tk.Radiobutton(parent, text="Normal", variable=OD_var, value="Normal")
    OD_option1.grid(row=row, column=0, padx=0, pady=5, sticky="w")
    OD_option2 = tk.Radiobutton(parent, text="Anormal", variable=OD_var, value="Anormal")
    OD_option2.grid(row=row, column=1, padx=10, pady=5, sticky="w")
    OD_comment.grid(row=row, column=2, padx=10, pady=5, sticky="w")

    if status == "normal": 
        OD_option1.config(command=lambda var=OD_var, entry=OD_comment, normal_text="Anormal": toggle_availability(var, entry, normal_text))
        OD_option2.config(command=lambda var=OD_var, entry=OD_comment, normal_text="Anormal": toggle_availability(var, entry, normal_text))
    else: 
        OD_option1.config(state=status)
        OD_option2.config(state=status)
        OD_comment.config(state="readonly")

    tk.Label(parent, text=topic).grid(row=row, column=3, padx=5, pady=2)

    OI_option1 = tk.Radiobutton(parent, text="Normal", variable=OI_var, value="Normal")
    OI_option1.grid(row=row, column=4, padx=0, pady=5, sticky="w")
    OI_option2 = tk.Radiobutton(parent, text="Anormal", variable=OI_var, value="Anormal")
    OI_option2.grid(row=row, column=5, padx=10, pady=5, sticky="w")
    OI_comment.grid(row=row, column=6, padx=10, pady=5, sticky="w")
    if status == "normal":  
        OI_option1.config(command=lambda var=OI_var, entry=OI_comment, normal_text="Anormal": toggle_availability(var, entry, normal_text))
        OI_option2.config(command=lambda var=OI_var, entry=OI_comment, normal_text="Anormal": toggle_availability(var, entry, normal_text))
    else: 
        OI_option1.config(state=status)
        OI_option2.config(state=status)
        OI_comment.config(state="readonly")
    

def search_name(workbook, name):
    sheet = workbook.active
    matches = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[2] and name.lower() in row[2].lower():
            matches.append(row)
    return matches

def data_to_dict(data): 
    return dict(zip(form.headers, data))

def format_date(date): 
    dt_obj = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
    return dt_obj.strftime("%Y/%m/%d")


# Update the canvas scrollregion dynamically
def update_scroll_region(event, canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Mouse wheel scrolling handler
def MouseWheelHandler(event, canvas):
    def delta(event):
        if event.num == 5 or event.delta < 0:
            return 1  # Scroll up
        return -1  # Scroll down

    canvas.yview_scroll(delta(event), "units")

def setup_window(root): 
    root.title("Student Records")
    root.bind("<Button-1>", focus_widget)
    root.resizable(True, True)
    root.minsize(1200, 700)

    # Create a canvas
    canvas = tk.Canvas(root)
    canvas.pack(fill="both", expand=True)

    # Create a frame inside the canvas
    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    content_frame.bind("<Configure>", lambda event:update_scroll_region(event, canvas))

    # Bind mouse wheel events
    root.bind("<MouseWheel>", lambda event: MouseWheelHandler(event, canvas))  # Windows/Linux
    root.bind("<Button-4>", lambda event: MouseWheelHandler(event, canvas))  # macOS Scroll Up
    root.bind("<Button-5>", lambda event: MouseWheelHandler(event, canvas))  # macOS Scroll Down

    return content_frame

def apply_font_to_all_widgets(frame, font_size):
    custom_font = font.Font(family="Helvetica", size=font_size)
    
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Text):  # Handle Text widget separately
            widget.tag_configure("all", font=custom_font)
            widget.config(wrap="word")  # Optional: Handle text wrapping
        else:
            try:
                widget.config(font=custom_font)
            except tk.TclError:
                pass  # Ignore widgets that don't support the 'font' attribute (if any)
