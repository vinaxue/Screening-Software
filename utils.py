import os
import tkinter as tk
from datetime import datetime
from tkinter import font, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

from database_form import create_form

######################## Form Utils ############################
def validate_vision_distance_input(P):
    if P == "" or P.startswith("20/"):
        return True
    return False

def update_text_input_timestamp(label, label_text, timestamp_var, text_var):
    time = datetime.now().strftime("%H:%M")
    if text_var.get() != "":
        timestamp_var.set(time)
        label.config(text=f"{label_text} @ tiempo {time}")
    else: 
        timestamp_var.set(time)
        label.config(text=label_text)

def update_checkbox_timestamp(timestamp_var, checkbox, checkbox_var, checkbox_text): 
    time = datetime.now().strftime("%H:%M")
    if checkbox_var.get(): 
        checkbox.config(text=f"{checkbox_text} @ tiempo {time}")
        timestamp_var.set(time)
    else: 
        checkbox.config(text=checkbox_text)
        timestamp_var.set("")

def focus_widget(event):
    widget = event.widget
    widget.focus_set()

def toggle_availability(var, entry, normal_text):
    if var.get() == normal_text: 
        entry.config(state="normal", bg="white")
    else: 
        entry.delete("1.0", tk.END)
        entry.config(state="disabled", bg="lightgray")

def format_date(date): 
    dt_obj = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    return dt_obj.strftime("%d/%m/%Y")

def generate_id(firstname, lastname, dob=""): 
    return "_".join([firstname.strip(), lastname.strip(), dob.strip()])    

def export_to_pdf(data):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(base_dir, "informes")
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    student_data = data["Student"]
    student_id = student_data[1]
    student_name = " ".join([student_data[2], student_data[3]])
    student_dob = student_data[4]
    student_phone = student_data[5]
    school_data = data["School"]
    school_name = school_data[1]
    creation_date = data["CreatedAt"]

    file_name = os.path.join(directory, f"Rx de anteojos - {student_name}.pdf")

    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
        # Margins
    margin_x = 50
    margin_y = 700

    # Title section
    c.setFont("Helvetica", 12)
    c.drawString(margin_x, margin_y + 50, f"Clínica/Escuela: {school_name}")
    c.drawString(margin_x + 300, margin_y + 50, f"Fecha: {creation_date}")
    c.drawString(margin_x, margin_y + 20, f"Nombre: {student_name}")
    c.drawString(margin_x + 300, margin_y + 20, f"Fecha de nacimiento: {student_dob}")
    c.drawString(margin_x, margin_y - 10, f"Número de teléfono: {student_phone}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, margin_y - 100, "Rx de anteojos")

    gp_data = data["GlassesPrescription"]
    gp_data_table = [
        ["", "Sphere", "Cylinder", "Axis", "dVA"],
        ["OD", gp_data[1], gp_data[3], gp_data[5], gp_data[7]],
        ["OI", gp_data[2], gp_data[4], gp_data[6], gp_data[8]],
        ["PD", f"{gp_data[9]}mm", "", "", ""]
    ]

    table = Table(gp_data_table, colWidths=[50, 100, 100, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, margin_x, margin_y - 200)

    # Signature section
    c.drawString(margin_x, margin_y - 250, "Firme de Doctor:")
    c.line(margin_x + 100, margin_y - 250, margin_x + 300, margin_y - 250)

    c.drawString(margin_x + 350, margin_y - 250, "Fecha:")
    c.line(margin_x + 400, margin_y - 250, margin_x + 500, margin_y - 250)

    c.save()
    success_message = f"Rx de anteojos se guardó correctamente como {file_name}."
    messagebox.showinfo("Éxito", success_message)

def update_table_radiobuttons(all_normal_var, var, comment_textbox):
    if all_normal_var.get() == 1:
        var.set("Normal") 
        comment_textbox.delete("1.0", tk.END)
        comment_textbox.config(state="disabled", bg="lightgray")

######################## Window Utils ############################

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
    root.title("Registros Estudiantiles")
    root.bind("<Button-1>", focus_widget)
    root.resizable(True, True)
    root.minsize(1280, 700)

    canvas = tk.Canvas(root)
    canvas.pack(fill="both", expand=True)

    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    content_frame.bind("<Configure>", lambda event:update_scroll_region(event, canvas))

    root.bind("<MouseWheel>", lambda event: MouseWheelHandler(event, canvas))  # Windows/Linux
    root.bind("<Button-4>", lambda event: MouseWheelHandler(event, canvas))  # macOS Scroll Up
    root.bind("<Button-5>", lambda event: MouseWheelHandler(event, canvas))  # macOS Scroll Down

    return content_frame

def apply_font_to_all_widgets(frame, font_size):
    custom_font = font.Font(family="Helvetica", size=font_size)
    
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Text):  
            widget.tag_configure("all", font=custom_font)
            widget.config(wrap="word") 
        else:
            try:
                widget.config(font=custom_font)
            except tk.TclError:
                pass  

def open_new_form(cur, record_data=None, student_data=None):
    form_window = tk.Toplevel()
    content_frame = setup_window(form_window)
    create_form(cur, form_window, content_frame, 0, record_data, student_data)