import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Software de evaluación escolar guatemalteco")
root.minsize(200, 300)

import search
import utils
import database as db

cur = db.connect_database()
db.create_tables(cur)

tk.Button(root, text="Ingresar Nuevo Registro", command=lambda cur=cur: utils.open_new_form(cur)).grid(row=0, column=0, columnspan=7, pady=10)
ttk.Separator(root, orient='horizontal').grid(row=1, column=0, padx=5, columnspan=7, pady=5, sticky="ew")

results_frame = tk.Frame(root)
search.create_search(cur, root, results_frame, 2)
results_frame.grid(row=5, column=0, columnspan=7, pady=20, padx=10, sticky="nsew")

root.mainloop()
