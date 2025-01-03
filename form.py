from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from openpyxl import Workbook, load_workbook
import form_utils as utils
import os

# Define form variables
school_var = tk.StringVar()
date_var = tk.StringVar()
name_var = tk.StringVar()
birthday_var = tk.StringVar()
phone_number_var = tk.StringVar()

distance_vision_var = tk.StringVar()
distance_vision_OD_var = tk.StringVar()
distance_vision_OI_var = tk.StringVar()

intraocular_pressure_var = tk.StringVar()
intraocular_pressure_OD_var = tk.StringVar()
intraocular_pressure_OI_var = tk.StringVar()
intraocular_pressure_timestamp_OD_var = tk.StringVar()
intraocular_pressure_timestamp_OI_var = tk.StringVar()

dilatation_var = tk.BooleanVar()
dilatation_timestamp_var = tk.StringVar()

refractive_status_method_var = tk.StringVar()
refractive_status_OD_var = tk.StringVar()
refractive_status_OD_dVA_var = tk.StringVar()
refractive_status_OI_var = tk.StringVar()
refractive_status_OI_dVA_var = tk.StringVar()

lens_prescription_OD_var = tk.StringVar()
lens_prescription_OI_var = tk.StringVar()

eyelid_OD_var = tk.StringVar()
eyelid_OI_var = tk.StringVar()
eyelid_OD_comments_var = tk.StringVar()
eyelid_OI_comments_var = tk.StringVar()

conjunctiva_OD_var = tk.StringVar()
conjunctiva_OI_var = tk.StringVar()
conjunctiva_OD_comments_var = tk.StringVar()
conjunctiva_OI_comments_var = tk.StringVar()

cornea_OD_var = tk.StringVar()
cornea_OI_var = tk.StringVar()
cornea_OD_comments_var = tk.StringVar()
cornea_OI_comments_var = tk.StringVar()

iris_OD_var = tk.StringVar()
iris_OI_var = tk.StringVar()
iris_OD_comments_var = tk.StringVar()
iris_OI_comments_var = tk.StringVar()

pupil_OD_var = tk.StringVar()
pupil_OI_var = tk.StringVar()
pupil_OD_comments_var = tk.StringVar()
pupil_OI_comments_var = tk.StringVar()

lente_OD_var = tk.StringVar()
lente_OI_var = tk.StringVar()
lente_OD_comments_var = tk.StringVar()
lente_OI_comments_var = tk.StringVar()

cd_OD_var = tk.StringVar()
cd_OI_var = tk.StringVar()

nerve_OD_var = tk.StringVar()
nerve_OI_var = tk.StringVar()
nerve_OD_comments_var = tk.StringVar()
nerve_OI_comments_var = tk.StringVar()

macula_OD_var = tk.StringVar()
macula_OI_var = tk.StringVar()
macula_OD_comments_var = tk.StringVar()
macula_OI_comments_var = tk.StringVar()

vasculature_OD_var = tk.StringVar()
vasculature_OI_var = tk.StringVar()
vasculature_OD_comments_var = tk.StringVar()
vasculature_OI_comments_var = tk.StringVar()

periphery_OD_var = tk.StringVar()
periphery_OI_var = tk.StringVar()
periphery_OD_comments_var = tk.StringVar()
periphery_OI_comments_var = tk.StringVar()

vitreous_OD_var = tk.StringVar()
vitreous_OI_var = tk.StringVar()
vitreous_OD_comments_var = tk.StringVar()
vitreous_OI_comments_var = tk.StringVar()

dx_myopia_var = tk.BooleanVar()
dx_hyperopia_var = tk.BooleanVar()
dx_astigmatism_var = tk.BooleanVar()

doctor_firm_var = tk.StringVar()
doctor_name_var = tk.StringVar()

def open_file(file_path): 
    # Create or load the workbook
    if not os.path.exists(file_path):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Student Data"
        # Add headers to the sheet
        sheet.append(["Clínica/Escuela", "Fecha", "Nombre", "Fecha_de_nacimiento", "Número_de_teléfono", "Razón_por_cita", 
                    "Visión_distancia", "Visión_distancia_OD", "Visión_distancia_OI", 
                    "Presión_intraocular", "Presión_intraocular_OD", "Presión_intraocular_OD_tiempo", "Presión_intraocular_OI", "Presión_intraocular_OI_tiempo", 
                    "Dilatación", "Dilatación_tiempo",
                    "Autorefraction/Retinoscopia", "Autorefraction/Retinoscopia_OD", "Autorefraction/Retinoscopia_OD_dVA", "Autorefraction/Retinoscopia_OI", "Autorefraction/Retinoscopia_OI_dVA",
                    "Rx_de_anteojos_OD", "Rx_de_anteojos_OI",
                    "Párpados_OD", "Párpados_OD_comments", "Párpados_OI", "Párpados_OI_comments",
                    "Conjunctiva_OD", "Conjunctiva_OD_comments", "Conjunctiva_OI", "Conjunctiva_OI_comments",
                    "Cornea_OD", "Cornea_OD_comments", "Cornea_OI", "Cornea_OI_comments",
                    "Iris_OD", "Iris_OD_comments", "Iris_OI", "Iris_OI_comments",
                    "Pupil_OD", "Pupil_OD_comments", "Pupil_OI", "Pupil_OI_comments",
                    "Lente_OD", "Lente_OD_comments", "Lente_OI", "Lente_OI_comments",
                    "C/D_OD", "C/D_OI", 
                    "Nervio_OD", "Nervio_OD_comments", "Nervio_OI", "Nervio_OI_comments",
                    "Macula_OD", "Macula_OD_comments", "Macula_OI", "Macula_OI_comments",
                    "Vasculatura_OD", "Vasculatura_OD_comments", "Vasculatura_OI", "vasculatura_OI_comments",
                    "Periferia_OD", "Periferia_OD_comments", "Periferia_OI", "Periferia_OI_comments",
                    "Vitreous_OD", "Vitreous_OD_comments", "Vitreous_OI", "vitreous_OI_comments",
                    "Dx_Miopía", "Dx_Hipermetropía", "Dx_Astigmatismo", "Dx_comments", "Tx",
                    "Firme_de_Doctor", "Nombre_de_Doctor", "Fecha_de_creación", "Fecha_de_la_última_edición"])
        workbook.save(file_path)
        return workbook
    else:
        workbook = load_workbook(file_path)
        sheet = workbook.active
        return workbook

def save_to_excel(workbook, file_path, mmhg_label_od, mmhg_label_oi, dilatation_checkbox, reason_for_visit_textbox, dx_comments_textbox, tx_textbox):
    """Saves form data to the Excel file."""
    school = school_var.get()
    date = date_var.get()
    name = name_var.get()
    birthday = birthday_var.get()
    phone_number = phone_number_var.get()
    reason_for_visit = reason_for_visit_textbox.get("1.0", tk.END).strip()

    distance_vision = distance_vision_var.get()
    distance_vision_OD = distance_vision_OD_var.get()
    distance_vision_OI = distance_vision_OI_var.get()

    intraocular_pressure = intraocular_pressure_var.get()
    intraocular_pressure_OD = intraocular_pressure_OD_var.get()
    intraocular_pressure_OI = intraocular_pressure_OI_var.get()
    intraocular_pressure_OD_timestamp = intraocular_pressure_timestamp_OD_var.get()
    intraocular_pressure_OI_timestamp = intraocular_pressure_timestamp_OI_var.get()

    dilatation = dilatation_var.get()
    dilatation_timestamp = dilatation_timestamp_var.get()

    refractive_status_method = refractive_status_method_var.get()
    refractive_status_OD = refractive_status_OD_var.get()
    refractive_status_OD_dVA = refractive_status_OD_dVA_var.get()
    refractive_status_OI = refractive_status_OI_var.get()
    refractive_status_OI_dVA = refractive_status_OI_dVA_var.get()

    lens_prescription_OD = lens_prescription_OD_var.get()
    lens_prescription_OI = lens_prescription_OI_var.get()

    eyelid_OD = eyelid_OD_var.get()
    eyelid_OI = eyelid_OI_var.get()
    eyelid_OD_comments = eyelid_OD_comments_var.get()
    eyelid_OI_comments = eyelid_OI_comments_var.get()

    conjunctiva_OD = conjunctiva_OD_var.get()
    conjunctiva_OI = conjunctiva_OI_var.get()
    conjunctiva_OD_comments = conjunctiva_OD_comments_var.get()
    conjunctiva_OI_comments = conjunctiva_OI_comments_var.get()

    cornea_OD = cornea_OD_var.get()
    cornea_OI = cornea_OI_var.get()
    cornea_OD_comments = cornea_OD_comments_var.get()
    cornea_OI_comments = cornea_OI_comments_var.get()

    iris_OD = iris_OD_var.get()
    iris_OI = iris_OI_var.get()
    iris_OD_comments = iris_OD_comments_var.get()
    iris_OI_comments = iris_OI_comments_var.get()

    pupil_OD = pupil_OD_var.get()
    pupil_OI = pupil_OI_var.get()
    pupil_OD_comments = pupil_OD_comments_var.get()
    pupil_OI_comments = pupil_OI_comments_var.get()

    lente_OD = lente_OD_var.get()
    lente_OI = lente_OI_var.get()
    lente_OD_comments = lente_OD_comments_var.get()
    lente_OI_comments = lente_OI_comments_var.get()

    cd_OD = cd_OD_var.get()
    cd_OI = cd_OI_var.get()

    nerve_OD = nerve_OD_var.get()
    nerve_OI = nerve_OI_var.get()
    nerve_OD_comments = nerve_OD_comments_var.get()
    nerve_OI_comments = nerve_OI_comments_var.get()

    macula_OD = macula_OD_var.get()
    macula_OI = macula_OI_var.get()
    macula_OD_comments = macula_OD_comments_var.get()
    macula_OI_comments = macula_OI_comments_var.get()

    vasculature_OD = vasculature_OD_var.get()
    vasculature_OI = vasculature_OI_var.get()
    vasculature_OD_comments = vasculature_OD_comments_var.get()
    vasculature_OI_comments = vasculature_OI_comments_var.get()

    periphery_OD = periphery_OD_var.get()
    periphery_OI = periphery_OI_var.get()
    periphery_OD_comments = periphery_OD_comments_var.get()
    periphery_OI_comments = periphery_OI_comments_var.get()

    vitreous_OD = vitreous_OD_var.get()
    vitreous_OI = vitreous_OI_var.get()
    vitreous_OD_comments = vitreous_OD_comments_var.get()
    vitreous_OI_comments = vitreous_OI_comments_var.get()

    dx_myopia = dx_myopia_var.get()
    dx_hyperopia = dx_hyperopia_var.get()
    dx_astigmatism = dx_astigmatism_var.get()
    dx_comments = dx_comments_textbox.get("1.0", tk.END).strip()
    tx = tx_textbox.get("1.0", tk.END).strip()
    
    doctor_firm = doctor_firm_var.get()
    doctor_name = doctor_name_var.get()
    creation_date = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    last_edit_date = datetime.now().strftime("%Y:%m:%d %H:%M:%S")

    if not school or not date or not name or not birthday or not phone_number:
        messagebox.showerror("Error", "Please fill in all required student information fields.")
        return

    if not distance_vision or not distance_vision_OD or not distance_vision_OI: 
        messagebox.showerror("Error", "Please fill in all required distance vision fields.")
        return
    
    if not intraocular_pressure or not intraocular_pressure_OD or not intraocular_pressure_OI: 
        messagebox.showerror("Error", "Please fill in all required intraocular pressure fields.")
        return
    
    if not refractive_status_method or not refractive_status_OD or not refractive_status_OD_dVA or not refractive_status_OI or not refractive_status_OI_dVA: 
        messagebox.showerror("Error", "Please fill in all required refractive status fields.")
        return
    
    if not eyelid_OD or not eyelid_OI or not conjunctiva_OD or not conjunctiva_OI or not cornea_OD or not cornea_OI or not iris_OD or not iris_OI or not pupil_OD or not pupil_OI or not lente_OD or not lente_OI or not nerve_OD or not nerve_OI or not macula_OD or not macula_OI or not vasculature_OD or not vasculature_OI or not periphery_OD or not periphery_OI or not vitreous_OD or not vitreous_OI: 
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    if not doctor_name or not doctor_firm: 
        messagebox.showerror("Error", "Please fill in all required doctor information fields.")
        return

    sheet = workbook.active
    sheet.append([school, date, name, birthday, phone_number, reason_for_visit, 
                  distance_vision, distance_vision_OD, distance_vision_OI, 
                  intraocular_pressure, intraocular_pressure_OD, intraocular_pressure_OD_timestamp, intraocular_pressure_OI, intraocular_pressure_OI_timestamp, 
                  dilatation, dilatation_timestamp, 
                  refractive_status_method, refractive_status_OD, refractive_status_OD_dVA, refractive_status_OI, refractive_status_OI_dVA, 
                  lens_prescription_OI, lens_prescription_OD, 
                  eyelid_OD, eyelid_OD_comments, eyelid_OI, eyelid_OI_comments, 
                  conjunctiva_OD, conjunctiva_OD_comments, conjunctiva_OI, conjunctiva_OI_comments,
                  cornea_OD, cornea_OD_comments, cornea_OI, cornea_OI_comments, 
                  iris_OD, iris_OD_comments, iris_OI, iris_OI_comments, 
                  pupil_OD, pupil_OD_comments, pupil_OI, pupil_OI_comments, 
                  lente_OD, lente_OD_comments, lente_OI, lente_OI_comments, 
                  cd_OD, cd_OI, 
                  nerve_OD, nerve_OD_comments, nerve_OI, nerve_OI_comments, 
                  macula_OD, macula_OD_comments, macula_OI, macula_OI_comments, 
                  vasculature_OD, vasculature_OD_comments, vasculature_OI, vasculature_OI_comments, 
                  periphery_OD, periphery_OD_comments, periphery_OI, periphery_OI_comments, 
                  vitreous_OD, vitreous_OD_comments, vitreous_OI, vitreous_OI_comments, 
                  dx_myopia, dx_hyperopia, dx_astigmatism, dx_comments, tx, 
                  doctor_firm, doctor_name, creation_date, last_edit_date])
    workbook.save(file_path)
    messagebox.showinfo("Success", "Data saved successfully!")

    # Clear the form
    school_var.set("")
    date_var.set("")
    name_var.set("")
    birthday_var.set("")
    phone_number_var.set("")
    reason_for_visit_textbox.delete("1.0", tk.END)

    distance_vision_var.set("")
    distance_vision_OD_var.set("20/")
    distance_vision_OI_var.set("20/")

    intraocular_pressure_var.set("")
    intraocular_pressure_OD_var.set("")
    intraocular_pressure_OI_var.set("")
    intraocular_pressure_timestamp_OD_var.set("")
    intraocular_pressure_timestamp_OI_var.set("")
    utils.update_text_input_timestamp(text_var=intraocular_pressure_OD_var, label=mmhg_label_od, label_text="mmHg", timestamp_var=intraocular_pressure_timestamp_OD_var)
    utils.update_text_input_timestamp(text_var=intraocular_pressure_OI_var, label=mmhg_label_oi, label_text="mmHg", timestamp_var=intraocular_pressure_timestamp_OI_var)

    dilatation_var.set(False)
    dilatation_timestamp_var.set("")
    utils.update_checkbox_timestamp(dilatation_timestamp_var, dilatation_checkbox, dilatation_var, "Dilatación")

    refractive_status_method_var.set("")
    refractive_status_OD_var.set("")
    refractive_status_OD_dVA_var.set("")
    refractive_status_OI_var.set("")
    refractive_status_OI_dVA_var.set("")

    lens_prescription_OD_var.set("")
    lens_prescription_OI_var.set("")

    eyelid_OD_var.set("")
    eyelid_OI_var.set("")
    eyelid_OD_comments_var.set("")
    eyelid_OI_comments_var.set("")

    conjunctiva_OD_var.set("")
    conjunctiva_OI_var.set("")
    conjunctiva_OD_comments_var.set("")
    conjunctiva_OI_comments_var.set("")

    cornea_OD_var.set("")
    cornea_OI_var.set("")
    cornea_OD_comments_var.set("")
    cornea_OI_comments_var.set("")

    iris_OD_var.set("")
    iris_OI_var.set("")
    iris_OD_comments_var.set("")
    iris_OI_comments_var.set("")

    pupil_OD_var.set("")
    pupil_OI_var.set("")
    pupil_OD_comments_var.set("")
    pupil_OI_comments_var.set("")

    lente_OD_var.set("")
    lente_OI_var.set("")
    lente_OD_comments_var.set("")
    lente_OI_comments_var.set("")

    cd_OD_var.set("")
    cd_OI_var.set("")

    nerve_OD_var.set("")
    nerve_OI_var.set("")
    nerve_OD_comments_var.set("")
    nerve_OI_comments_var.set("")

    macula_OD_var.set("")
    macula_OI_var.set("")
    macula_OD_comments_var.set("")
    macula_OI_comments_var.set("")

    vasculature_OD_var.set("")
    vasculature_OI_var.set("")
    vasculature_OD_comments_var.set("")
    vasculature_OI_comments_var.set("")

    periphery_OD_var.set("")
    periphery_OI_var.set("")
    periphery_OD_comments_var.set("")
    periphery_OI_comments_var.set("")

    vitreous_OD_var.set("")
    vitreous_OI_var.set("")
    vitreous_OD_comments_var.set("")
    vitreous_OI_comments_var.set("")

    dx_myopia_var.set(False)
    dx_hyperopia_var.set(False)
    dx_astigmatism_var.set(False)
    dx_comments_textbox.delete("1.0", tk.END)
    tx_textbox.delete("1.0", tk.END)

    doctor_firm_var.set("")
    doctor_name_var.set("")

def create_form(workbook, content_frame, file_path):

    # Create form labels and entry fields

    ######################## student information ###############################
    tk.Label(content_frame, text="Clínica/Escuela:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(content_frame, textvariable=school_var).grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="we")

    tk.Label(content_frame, text="Fecha:").grid(row=0, column=4, padx=10, pady=5, sticky="w")
    tk.Entry(content_frame, textvariable=date_var).grid(row=0, column=5, columnspan=2, padx=10, pady=5, sticky="we")

    tk.Label(content_frame, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(content_frame, textvariable=name_var).grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="we")

    tk.Label(content_frame, text="Fecha de nacimiento:").grid(row=1, column=4, padx=10, pady=5, sticky="w")
    tk.Entry(content_frame, textvariable=birthday_var).grid(row=1, column=5, columnspan=3, padx=10, pady=5, sticky="we")

    tk.Label(content_frame, text="Número de teléfono:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(content_frame, textvariable=phone_number_var).grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="we")

    tk.Label(content_frame, text="Razón por cita:").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
    reason_for_visit_textbox = tk.Text(content_frame, height=5, width=60)
    reason_for_visit_textbox.grid(row=3, column=1, columnspan=6, padx=10, pady=5, sticky="w")

    ######################## vision distance ###############################
    tk.Label(content_frame, text="Visión distancia(dVA):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    vd_option1 = tk.Radiobutton(content_frame, text="s/c", variable=distance_vision_var, value="s/c")
    vd_option1.grid(row=4, column=1, padx=10, pady=5, sticky="w")
    vd_option2 = tk.Radiobutton(content_frame, text="c/c", variable=distance_vision_var, value="c/c")
    vd_option2.grid(row=4, column=2, padx=10, pady=5, sticky="w")

    vision_distance_validate_command = content_frame.register(utils.validate_vision_distance_input) 

    tk.Label(content_frame, text="OD:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    vd_entry_od = tk.Entry(content_frame, textvariable=distance_vision_OD_var, width=10, validate="key", validatecommand=(vision_distance_validate_command, "%P"))
    vd_entry_od.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    vd_entry_od.insert(0, "20/") 

    tk.Label(content_frame, text="OI:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    vd_entry_oi = tk.Entry(content_frame, textvariable=distance_vision_OI_var, width=10, validate="key", validatecommand=(vision_distance_validate_command, "%P"))
    vd_entry_oi.grid(row=6, column=1, padx=10, pady=5, sticky="w")
    vd_entry_oi.insert(0, "20/") 


    ######################## intraocular pressure ###############################
    tk.Label(content_frame, text="Presión intraocular:").grid(row=4, column=4, padx=10, pady=5, sticky="w")
    ip_option1 = tk.Radiobutton(content_frame, text="iCare", variable=intraocular_pressure_var, value="iCare")
    ip_option1.grid(row=4, column=5, padx=10, pady=5, sticky="w")
    ip_option2 = tk.Radiobutton(content_frame, text="GAT", variable=intraocular_pressure_var, value="GAT")
    ip_option2.grid(row=4, column=6, padx=10, pady=5, sticky="w")

    tk.Label(content_frame, text="OD:").grid(row=5, column=4, padx=10, pady=5, sticky="w")
    ip_entry_od = tk.Entry(content_frame, textvariable=intraocular_pressure_OD_var, width=10)
    ip_entry_od.grid(row=5, column=5, padx=10, pady=5, sticky="w")
    mmhg_label_od = tk.Label(content_frame, text="mmHg")
    mmhg_label_od.grid(row=5, column=6, padx=0, pady=5, sticky="w")

    tk.Label(content_frame, text="OI:").grid(row=6, column=4, padx=10, pady=5, sticky="w")
    ip_entry_oi = tk.Entry(content_frame, textvariable=intraocular_pressure_OI_var, width=10)
    ip_entry_oi.grid(row=6, column=5, padx=10, pady=5, sticky="w")
    mmhg_label_oi = tk.Label(content_frame, text="mmHg")
    mmhg_label_oi.grid(row=6, column=6, padx=0, pady=5, sticky="w")

    ip_entry_od.bind("<FocusOut>", lambda event, text_var=intraocular_pressure_OD_var, label=mmhg_label_od, label_text="mmHg", timestamp_var=intraocular_pressure_timestamp_OD_var: utils.update_text_input_timestamp(label, label_text, timestamp_var, text_var))
    ip_entry_oi.bind("<FocusOut>", lambda event, text_var=intraocular_pressure_OI_var, label=mmhg_label_oi, label_text="mmHg", timestamp_var=intraocular_pressure_timestamp_OI_var: utils.update_text_input_timestamp(label, label_text, timestamp_var, text_var))


    ######################## dilatation ###############################
    dilatation_checkbox = tk.Checkbutton(content_frame, text="Dilatación", variable=dilatation_var)
    dilatation_checkbox.config(command=lambda checkbox_text="Dilatación", timestamp_var=dilatation_timestamp_var, checkbox_var=dilatation_var, checkbox=dilatation_checkbox: utils.update_checkbox_timestamp(timestamp_var, checkbox, checkbox_var, checkbox_text))
    dilatation_checkbox.grid(row=7, column=0, padx=5, pady=5, sticky="w")


    ######################## refractive status ###############################
    rs_option1 = tk.Radiobutton(content_frame, text="Autorefraction", variable=refractive_status_method_var, value="Autorefraction")
    rs_option1.grid(row=8, column=0, padx=0, pady=5, sticky="w")
    rs_option2 = tk.Radiobutton(content_frame, text="Retinoscopia", variable=refractive_status_method_var, value="Retinoscopia")
    rs_option2.grid(row=8, column=1, padx=10, pady=5, sticky="w")

    tk.Label(content_frame, text="OD:").grid(row=9, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(content_frame, textvariable=refractive_status_OD_var, width=10).grid(row=9, column=1, padx=10, pady=5, sticky="w")

    tk.Label(content_frame, text="dVA:").grid(row=10, column=0, padx=20, pady=5, sticky="w")
    vd_entry_od = tk.Entry(content_frame, textvariable=refractive_status_OD_dVA_var, width=10, validate="key", validatecommand=(vision_distance_validate_command, "%P"))
    vd_entry_od.grid(row=10, column=1, padx=10, pady=5, sticky="w")
    vd_entry_od.insert(0, "20/") 

    tk.Label(content_frame, text="OI:").grid(row=11, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(content_frame, textvariable=refractive_status_OI_var, width=10).grid(row=11, column=1, padx=10, pady=5, sticky="w")

    tk.Label(content_frame, text="dVA:").grid(row=12, column=0, padx=20, pady=5, sticky="w")
    vd_entry_oi = tk.Entry(content_frame, textvariable=refractive_status_OI_dVA_var, width=10, validate="key", validatecommand=(vision_distance_validate_command, "%P"))
    vd_entry_oi.grid(row=12, column=1, padx=10, pady=5, sticky="w")
    vd_entry_oi.insert(0, "20/") 


    ######################## lens prescription ###############################
    tk.Label(content_frame, text="Rx de anteojos").grid(row=8, column=4, padx=10, pady=5, sticky="w")

    tk.Label(content_frame, text="OD:").grid(row=9, column=4, padx=10, pady=5, sticky="w")
    tk.Entry(content_frame, textvariable=lens_prescription_OD_var, width=10).grid(row=9, column=5, padx=10, pady=5, sticky="w")

    tk.Label(content_frame, text="OI:").grid(row=10, column=4, padx=10, pady=5, sticky="w")
    tk.Entry(content_frame, textvariable=lens_prescription_OI_var, width=10).grid(row=10, column=5, padx=10, pady=5, sticky="w")


    ######################## table ###############################
    tk.Label(content_frame, text="OD").grid(row=13, column=0, columnspan=3)
    tk.Label(content_frame, text="OI").grid(row=13, column=4, columnspan=3)
    utils.create_row(content_frame, "Párpados", eyelid_OD_var, eyelid_OD_comments_var, eyelid_OI_var, eyelid_OI_comments_var, 14)
    utils.create_row(content_frame, "Conjunctiva", conjunctiva_OD_var, conjunctiva_OD_comments_var, conjunctiva_OI_var, conjunctiva_OI_comments_var, 15)
    utils.create_row(content_frame, "Cornea", cornea_OD_var, cornea_OD_comments_var, cornea_OI_var, cornea_OI_comments_var, 16)
    utils.create_row(content_frame, "Iris", iris_OD_var, iris_OD_comments_var, iris_OI_var, iris_OI_comments_var, 17)
    utils.create_row(content_frame, "Pupil", pupil_OD_var, pupil_OD_comments_var, pupil_OI_var, pupil_OI_comments_var, 18)
    utils.create_row(content_frame, "Lente", lente_OD_var, lente_OD_comments_var, lente_OI_var, lente_OI_comments_var, 19)
    tk.Label(content_frame, text="OD").grid(row=20, column=0, columnspan=3)
    tk.Label(content_frame, text="OI").grid(row=20, column=4, columnspan=3)

    tk.Entry(content_frame, textvariable=cd_OD_var, width=10).grid(row=21, column=0, columnspan=3, padx=10, pady=5, sticky="we")
    tk.Label(content_frame, text="C/D").grid(row=21, column=3, padx=5, pady=2)
    tk.Entry(content_frame, textvariable=cd_OI_var, width=10).grid(row=21, column=4, columnspan=3, padx=10, pady=5, sticky="we")

    utils.create_row(content_frame, "Nervio", nerve_OD_var, nerve_OD_comments_var, nerve_OI_var, nerve_OI_comments_var, 22)
    utils.create_row(content_frame, "Macula", macula_OD_var, macula_OD_comments_var, macula_OI_var, macula_OI_comments_var, 23)
    utils.create_row(content_frame, "Vasculatura", vasculature_OD_var, vasculature_OD_comments_var, vasculature_OI_var, vasculature_OI_comments_var, 24)
    utils.create_row(content_frame, "Periferia", periphery_OD_var, periphery_OD_comments_var, periphery_OI_var, periphery_OI_comments_var, 25)
    utils.create_row(content_frame, "Vitreous", vitreous_OD_var, vitreous_OD_comments_var, vitreous_OI_var, vitreous_OI_comments_var, 26)


    ######################## diagnosis ###############################
    tk.Label(content_frame, text="Dx:").grid(row=27, column=0, sticky="w")
    tk.Checkbutton(content_frame, text="Miopía", variable=dx_myopia_var).grid(row=27, column=1, sticky="w")
    tk.Checkbutton(content_frame, text="Hipermetropía", variable=dx_hyperopia_var).grid(row=27, column=2, sticky="w")
    tk.Checkbutton(content_frame, text="Astigmatismo", variable=dx_astigmatism_var).grid(row=27, column=3, sticky="w")
    dx_comments_textbox = tk.Text(content_frame, height=3, width=60)
    dx_comments_textbox.grid(row=28, column=1, columnspan=6, padx=10, pady=5, sticky="w")

    tk.Label(content_frame, text="Tx:").grid(row=29, column=0, sticky="nw")
    tx_textbox = tk.Text(content_frame, height=3, width=60)
    tx_textbox.grid(row=29, column=1, columnspan=6, padx=10, pady=5, sticky="w")

    ######################## doctor information ###############################
    tk.Label(content_frame, text="Firme de Doctor:").grid(row=30, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(content_frame, textvariable=doctor_firm_var, width=10).grid(row=30, column=1, columnspan=2, padx=10, pady=5, sticky="we")
    tk.Label(content_frame, text="Nombre de Doctor:").grid(row=31, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(content_frame, textvariable=doctor_name_var, width=10).grid(row=31, column=1, columnspan=2, padx=10, pady=5, sticky="we")
    creation_date = datetime.now().strftime("%Y:%m:%d")
    tk.Label(content_frame, text=f"Fecha: {creation_date}").grid(row=31, column=6, padx=10, pady=5, sticky="w")


    # Save button
    tk.Button(content_frame, text="Save", command=lambda: save_to_excel(workbook, file_path, mmhg_label_od, mmhg_label_oi, dilatation_checkbox, reason_for_visit_textbox, dx_comments_textbox, tx_textbox)).grid(row=32, column=0, columnspan=7, pady=10)
