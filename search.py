import tkinter as tk
from tkinter import messagebox
import utils
import database as db
from form_components import EntryWithPlaceholder

def open_record(cur, results_frame, record_data=None, student_data=None):
    for widget in results_frame.winfo_children():
        widget.destroy()
    utils.open_new_form(cur, record_data, student_data)

def perform_search(cur, firstname_search_entry, lastname_search_entry, dob_search_entry, results_frame):
    firstname = firstname_search_entry.get()
    lastname = lastname_search_entry.get()
    dob = dob_search_entry.get()

    if firstname == "" or lastname == "" or dob == "":
        messagebox.showerror("Error", "Por favor ingrese todos los campos.")
        return

    for widget in results_frame.winfo_children():
        widget.destroy()

    search_results = db.fetch_record(cur, firstname, lastname, dob)

    for col in range(7):
        tk.Label(results_frame, text=" ", width=10).grid(row=1, column=col)

    if search_results != []: 
        tk.Label(results_frame, text="#", font=("Helvetica", 10, "bold"), bg="lightgray").grid(row=2, column=1, padx=5, pady=5, sticky="w")
        tk.Label(results_frame, text="Clínica/Escuela", font=("Helvetica", 10, "bold"), bg="lightgray").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        tk.Label(results_frame, text="Nombre", font=("Helvetica", 10, "bold"), bg="lightgray").grid(row=2, column=3, padx=5, pady=5, sticky="w")
        tk.Label(results_frame, text="Fecha de nacimiento", font=("Helvetica", 10, "bold"), bg="lightgray").grid(row=2, column=4, padx=5, pady=5, sticky="w")
        tk.Label(results_frame, text="Acción", font=("Helvetica", 10, "bold"), bg="lightgray").grid(row=2, column=5, padx=5, pady=5, sticky="w")

        tk.Button(results_frame, text=f"Ingresar Nuevo Registro por {firstname} {lastname}", 
                command=lambda cur=cur, results_frame=results_frame, student_data=search_results[0]["Student"]: open_record(cur, results_frame, student_data=student_data)).grid(
                    row=0, column=0, columnspan=7, padx=5, pady=5)
    else: 
        tk.Label(results_frame, text="No se pudieron encontrar resultados.").grid(row=2, column=0, columnspan=7, padx=5, pady=5)

    for idx, result in enumerate(search_results):
        school = result["School"]
        student = result["Student"]
        tk.Label(results_frame, text=f"{idx+1}").grid(row=idx+3, column=1, padx=5, pady=5, sticky="w")
        tk.Label(results_frame, text=f"{school[1]}").grid(row=idx+3, column=2, padx=5, pady=5, sticky="w")
        tk.Label(results_frame, text=f"{student[2]} {student[3]}").grid(row=idx+3, column=3, padx=5, pady=5, sticky="w")
        tk.Label(results_frame, text=f"{student[4]}").grid(row=idx+3, column=4, padx=5, pady=5, sticky="w")
        tk.Button(results_frame, text="Ver/Editar", 
                  command=lambda cur=cur, record_data=result, results_frame=results_frame: open_record(cur, results_frame, record_data)).grid(
                    row=idx+3, column=5, padx=5, pady=5, sticky="w")

def create_search(cur, content_frame, results_frame, row): 
    for col in range(7):
        tk.Label(content_frame, text=" ", width=10).grid(row=row, column=col)

    tk.Label(content_frame, text="Nombre: ").grid(row=row+1, column=1, padx=5, pady=5, sticky="w")
    firstname_search_entry = tk.Entry(content_frame)
    firstname_search_entry.grid(row=row+1, column=2, padx=5, pady=5, sticky="we")

    tk.Label(content_frame, text="Apellido: ").grid(row=row+1, column=3, padx=5, pady=5, sticky="w")
    lastname_search_entry = tk.Entry(content_frame, width=20)
    lastname_search_entry.grid(row=row+1, column=4, padx=5, pady=5, sticky="we")

    tk.Label(content_frame, text="Fecha de nacimiento: ").grid(row=row+2, column=1, padx=5, pady=5, sticky="w")
    dob_search_entry = EntryWithPlaceholder(content_frame, placeholder="dd/mm/aaaa")
    dob_search_entry.grid(row=row+2, column=2, padx=5, pady=5, sticky="we")

    search_button = tk.Button(content_frame, text="Busca", command=lambda: perform_search(cur, firstname_search_entry, lastname_search_entry, dob_search_entry, results_frame))
    search_button.grid(row=row+1, column=5, padx=5, pady=5)

    def clear_search_form(): 
        firstname_search_entry.delete(0, tk.END)
        lastname_search_entry.delete(0, tk.END)
        dob_search_entry.delete(0, tk.END)

    clear_button = tk.Button(content_frame, text="Borrar", command=lambda: clear_search_form())
    clear_button.grid(row=row+2, column=5, padx=5, pady=5)

    tk.Label(content_frame, text="").grid(row=row+1, column=6, padx=5, pady=5, sticky="w")