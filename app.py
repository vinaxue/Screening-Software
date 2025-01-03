import tkinter as tk

# Define the Excel file path
EXCEL_FILE = "Guatemalan_school_screening_form.xlsx"

# Create the main window
root = tk.Tk()

import form 
import form_utils as utils

root.title("Input Form")
root.bind("<Button-1>", utils.focus_widget)
root.resizable(True, True)
root.minsize(1000, 700)

# Create a canvas
canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)

# Create a frame inside the canvas
content_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Update the canvas scrollregion dynamically
def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

content_frame.bind("<Configure>", update_scroll_region)

# Mouse wheel scrolling handler
def MouseWheelHandler(event):
    def delta(event):
        if event.num == 5 or event.delta < 0:
            return 1  # Scroll up
        return -1  # Scroll down

    canvas.yview_scroll(delta(event), "units")

# Bind mouse wheel events
root.bind("<MouseWheel>", MouseWheelHandler)  # Windows/Linux
root.bind("<Button-4>", MouseWheelHandler)  # macOS Scroll Up
root.bind("<Button-5>", MouseWheelHandler)  # macOS Scroll Down


workbook = form.open_file(EXCEL_FILE)
form.create_form(workbook, content_frame, EXCEL_FILE)

root.mainloop()
