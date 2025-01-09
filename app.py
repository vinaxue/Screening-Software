import tkinter as tk

# Define the Excel file path
EXCEL_FILE = "Guatemalan_school_screening_form.xlsx"

# Create the main window
root = tk.Tk()

import form 
import search
import utils

content_frame = utils.setup_window(root)

workbook = form.open_file(EXCEL_FILE)
search.create_search(workbook, content_frame, EXCEL_FILE)

root.mainloop()
