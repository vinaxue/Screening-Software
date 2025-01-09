import tkinter as tk
from tkinter import messagebox, Toplevel
import form
import utils

def view_edit_record(results_frame, workbook, data, row_index, file_path, row):
    for widget in results_frame.winfo_children():
        widget.destroy()
        
    form_window = Toplevel()
    content_frame = utils.setup_window(form_window)
    
    form.data_fill_form(form_window, workbook, content_frame, file_path, row, data, row_index)


def create_search_result_table(workbook, results_frame, results, file_path):
    for widget in results_frame.winfo_children():
        widget.destroy()

    headers = ["#", "Clínica/Escuela", "Nombre", "Fecha_de_creación", "Fecha_de_la_última_edición", "Acción"]
    for col, header in enumerate(headers):
        header_label = tk.Label(results_frame, text=header, bg="lightgrey")
        header_label.grid(row=0, column=col, padx=5, pady=5, sticky="w")

    for row_index, result in enumerate(results, start=1):
        data_dict = utils.data_to_dict(result)
        row_data = [
            row_index,  # Index
            data_dict["Clínica/Escuela"],
            data_dict["Nombre"],
            utils.format_date(data_dict["Fecha_de_creación"]),
            utils.format_date(data_dict["Fecha_de_la_última_edición"]),
        ]
        for col, data in enumerate(row_data):
            cell_label = tk.Label(results_frame, text=data, font=("Arial", 10), anchor="w")
            cell_label.grid(row=row_index, column=col, padx=5, pady=5, sticky="w")
        
        view_edit_button = tk.Button(
            results_frame, 
            text="View/Edit", 
            command=lambda data=data_dict, row=row_index: view_edit_record(results_frame, workbook, data, row, file_path, 0)
        )
        view_edit_button.grid(row=row_index, column=len(headers) - 1, padx=5, pady=5, sticky="ew")
    
def perform_search(workbook, search_entry, results_frame, file_path):
    name = search_entry.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a name to search.")
        return

    matches = utils.search_name(workbook, name)
    for widget in results_frame.winfo_children():
        widget.destroy()

    if matches:
        tk.Label(results_frame, text=f"Found {len(matches)} match(es):", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        create_search_result_table(workbook, results_frame, matches, file_path)
        search_entry.delete(0, tk.END)
    else:
        tk.Label(results_frame, text="No matches found. Please fill the form below:", font=("Arial", 12)).grid(row=0, column=0, columnspan=7, sticky="w", padx=5, pady=5)
        form.create_form(workbook, results_frame, file_path, 1)
        search_entry.delete(0, tk.END)
    
    utils.apply_font_to_all_widgets(results_frame, 12)


def create_search(workbook, content_frame, file_path): 
    for col in range(7):
        tk.Label(content_frame, text=" ", width=10).grid(row=0, column=col)

    search_label = tk.Label(content_frame, text="Search by Name:")
    search_label.grid(row=1, column=2, padx=5, pady=5)

    search_entry = tk.Entry(content_frame, width=30)
    search_entry.grid(row=1, column=3, padx=5, pady=5)

    results_frame = tk.Frame(content_frame)

    search_button = tk.Button(content_frame, text="Search", command=lambda: perform_search(workbook, search_entry, results_frame, file_path))
    search_button.grid(row=1, column=4, padx=5, pady=5)

    results_frame.grid(row=2, column=0, columnspan=7, pady=20, padx=10, sticky="nsew")

    utils.apply_font_to_all_widgets(content_frame, 14)