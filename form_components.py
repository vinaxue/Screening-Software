import tkinter as tk
from tkinter import ttk
import utils

def create_label_and_entry(content_frame, label_text, row, col_start, col_span_entry=1, default_value=None, prefill_value=None):
    label = tk.Label(content_frame, text=label_text)
    label.grid(row=row, column=col_start, padx=10, pady=5, sticky="w")
    entry_widget = tk.Entry(content_frame)
    entry_widget.grid(row=row, column=col_start+1, columnspan=col_span_entry, padx=10, pady=5, sticky="we")
    if prefill_value: 
        entry_widget.insert(0, prefill_value)
        entry_widget.config(state="readonly")
    elif default_value:
        entry_widget.insert(0, default_value)
    return entry_widget, label

def create_label_and_text(content_frame, row_start, col_span = 1, height=3, width=60, label_text = None, prefill_value=""):
    if label_text: 
        label = tk.Label(content_frame, text=label_text)
        label.grid(row=row_start, column=0, columnspan=col_span, padx=10, pady=5, sticky="nw")
    else: 
        label = None
    text_widget = tk.Text(content_frame, height=height, width=width)
    text_widget.grid(row=row_start, column=1, columnspan=col_span, padx=10, pady=5, sticky="w")
    if prefill_value != "": 
        text_widget.insert("1.0", prefill_value)
        text_widget.config(state="disabled", bg="lightgray")

    return text_widget, label

def create_label_and_radiobuttons(content_frame, row, col_start, options, variable, label_text = None, button_align="w", disabled = False):
    if label_text: 
        tk.Label(content_frame, text=label_text).grid(row=row, column=col_start, padx=10, pady=5, sticky="w")
    else: 
        col_start -= 1
    radiobuttons = []
    for idx, (text, value) in enumerate(options.items()):
        radiobutton = ttk.Radiobutton(content_frame, text=text, variable=variable, value=value, state="disabled" if disabled else "normal")
        radiobutton.grid(row=row, column=col_start+1+idx, padx=10, pady=5, sticky=button_align)
        radiobuttons.append(radiobutton)
    return radiobuttons

def create_intraocular_pressure_section(content_frame, count, row, data=None):
    tk.Label(content_frame, text=f"#{count}").grid(row=row, column=0, padx=10, pady=5, sticky="w")
    ip_options = {
        "iCare": "iCare", 
        "GAT": "GAT"
    }
    ip_method_var = tk.StringVar()
    ip_disable_radiobuttons = False
    ip_timestamp_od_var = tk.StringVar()
    ip_timestamp_oi_var = tk.StringVar()

    if data: 
        ip_method_var.set(data[1])
        ip_disable_radiobuttons = True
        ip_od_prefill = data[2]
        ip_timestamp_od_var.set(data[3])
        ip_oi_prefill = data[4]
        ip_timestamp_oi_var.set(data[5])
    else: 
        ip_od_prefill = None
        ip_oi_prefill = None

    ip_radiobuttons = create_label_and_radiobuttons(content_frame, row, 1, ip_options, ip_method_var, "Presión intraocular:", disabled=ip_disable_radiobuttons) # row, col_start, options, variable

    ip_entry_od, ip_entry_od_label = create_label_and_entry(content_frame, "OD:", row+1, 1, 1, prefill_value=ip_od_prefill) # row, col_start, colspan_label, colspan_entry
    mmhg_label_od = tk.Label(content_frame, text=f"mmHg @ tiempo {ip_timestamp_od_var.get()}" if data else "mmHg")
    mmhg_label_od.grid(row=row+1, column=3, padx=0, pady=5, sticky="w")

    ip_entry_oi, ip_entry_oi_label = create_label_and_entry(content_frame, "OI:", row+2, 1, 1, prefill_value=ip_oi_prefill) # row, col_start, colspan_label, colspan_entry
    mmhg_label_oi = tk.Label(content_frame, text=f"mmHg @ tiempo {ip_timestamp_oi_var.get()}" if data else "mmHg")
    mmhg_label_oi.grid(row=row+2, column=3, padx=0, pady=5, sticky="w")

    if not data: 
        ip_entry_od.bind("<FocusOut>", lambda event, text_var=ip_entry_od, label=mmhg_label_od, label_text="mmHg", timestamp_var=ip_timestamp_od_var: utils.update_text_input_timestamp(label, label_text, timestamp_var, text_var))
        ip_entry_oi.bind("<FocusOut>", lambda event, text_var=ip_entry_oi, label=mmhg_label_oi, label_text="mmHg", timestamp_var=ip_timestamp_oi_var: utils.update_text_input_timestamp(label, label_text, timestamp_var, text_var))

    return ip_method_var, ip_radiobuttons, ip_entry_od, ip_timestamp_od_var, ip_entry_oi, ip_timestamp_oi_var

def create_table(content_frame, row, col_start, row_headers, col_headers):
    col_labels = []
    row_labels = []
    col = col_start
    for header in col_headers: 
        col += 1
        label = tk.Label(content_frame, text=header, font=("Helvetica", 10, "bold"))
        label.grid(row=row, column=col, padx=10, pady=5, sticky="w")
        col_labels.append(label)
    for header in row_headers: 
        row += 1
        label = tk.Label(content_frame, text=header, font=("Helvetica", 10, "bold"))
        label.grid(row=row, column=col_start, padx=10, pady=5, sticky="w")
        row_labels.append(label)
    return col_labels, row_labels

def create_row(parent, topic, od_comment, oi_comment, row, all_normal_od_var, all_normal_oi_var, status="normal", od_data=None, oi_data=None): 
    od_var = tk.StringVar()
    oi_var = tk.StringVar()
    options = {
        "Normal": "Normal",
        "Anormal": "Anormal"
    }

    if od_data and oi_data: 
        od_var.set(od_data)
        oi_var.set(oi_data)

    od_radiobuttons = create_label_and_radiobuttons(parent, row, 1, options, od_var, button_align="e", disabled=od_data) # row, col_start, options, variable
    od_comment.grid(row=row+1, column=0, columnspan=3, padx=10, pady=5, sticky="e")

    if status == "normal": 
        od_radiobuttons[0].config(command=lambda var=od_var, entry=od_comment, normal_text="Anormal": utils.toggle_availability(var, entry, normal_text))
        od_radiobuttons[1].config(command=lambda var=od_var, entry=od_comment, normal_text="Anormal": utils.toggle_availability(var, entry, normal_text))
    else: 
        od_radiobuttons[0].config(state=status)
        od_radiobuttons[1].config(state=status)
        od_comment.config(state="disabled")

    label = tk.Label(parent, text=topic, font=("Helvetica", 10, "bold"))
    label.grid(row=row, column=3, padx=5, pady=2, sticky="n")

    oi_radiobuttons = create_label_and_radiobuttons(parent, row, 4, options, oi_var, button_align="w", disabled=oi_data) # row, col_start, options, variable
    oi_comment.grid(row=row+1, column=4, columnspan=3, padx=10, pady=5, sticky="w")

    if status == "normal":  
        oi_radiobuttons[0].config(command=lambda var=oi_var, entry=oi_comment, normal_text="Anormal": utils.toggle_availability(var, entry, normal_text))
        oi_radiobuttons[1].config(command=lambda var=oi_var, entry=oi_comment, normal_text="Anormal": utils.toggle_availability(var, entry, normal_text))
    else: 
        oi_radiobuttons[0].config(state=status)
        oi_radiobuttons[1].config(state=status)
        oi_comment.config(state="disabled")
    
    all_normal_od_var.trace("w", lambda *args: utils.update_table_radiobuttons(all_normal_od_var, od_var, od_comment))
    all_normal_oi_var.trace("w", lambda *args: utils.update_table_radiobuttons(all_normal_oi_var, oi_var, oi_comment))

    return od_var, oi_var, od_radiobuttons, oi_radiobuttons, label

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()