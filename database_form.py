from datetime import datetime
from tkinter import messagebox, ttk
from form_components import *
import database as db
import tkinter as tk

import utils

def create_form(cur, window, content_frame, row, 
                record_data=None, student_data=None):
    creation_date = datetime.now().strftime("%d/%m/%Y")

    ######################## student information ###############################
    if record_data:
        student_record_data = record_data["Student"]
        firstname_prefill = student_record_data[2]
        lastname_prefill = student_record_data[3]
        dob_prefill = student_record_data[4]
        phone_number_prefill = student_record_data[5]

        school_data = record_data["School"]
        school_prefill = school_data[1]

        rfv_prefill = record_data["ReasonForVisit"]
    elif student_data: 
        firstname_prefill = student_data[2]
        lastname_prefill = student_data[3]
        dob_prefill = student_data[4]
        phone_number_prefill = student_data[5]
        school_id = student_data[6]
        school_row = db.fetch_row(cur, "School", "_rowid_", school_id)
        school_prefill = school_row[1]

        rfv_prefill = ""
    else:
        firstname_prefill = lastname_prefill = dob_prefill = phone_number_prefill = school_prefill = None
        rfv_prefill = ""

    school_entry, school_label = create_label_and_entry(content_frame, "Clínica/Escuela:", row, 0, 2, prefill_value=school_prefill) # row, col_start, colspan_entry
    tk.Label(content_frame, text=f"Fecha: {creation_date}").grid(row=row, column=4, columnspan=2, padx=10, pady=5, sticky="w")
    firstname_entry, firstname_label = create_label_and_entry(content_frame, "Nombre:", row+1, 0, 1, prefill_value=firstname_prefill)
    lastname_entry, lastname_label = create_label_and_entry(content_frame, "Apellido:", row+1, 2, 1, prefill_value=lastname_prefill)
    
    tk.Label(content_frame, text="Fecha de nacimiento:").grid(row=row+1, column=4, padx=10, pady=5, sticky="w")
    if dob_prefill:
        dob_entry = tk.Entry(content_frame)
        dob_entry.insert(0, dob_prefill)
        dob_entry.config(state="readonly")
    else:
        dob_entry = EntryWithPlaceholder(content_frame, "dd/mm/aaaa")

    dob_entry.grid(row=row+1, column=5, padx=10, pady=5, sticky="we")

    phone_number_entry, phone_number_label = create_label_and_entry(content_frame, "Número de teléfono:", row+2, 0, 2, prefill_value=phone_number_prefill)
    reason_for_visit_entry, rfv_label = create_label_and_text(content_frame, row+3, 7, label_text="Razón por cita:", width=100, prefill_value=rfv_prefill) # row_start, col_span

    separator_1 = ttk.Separator(content_frame, orient='horizontal')
    separator_1.grid(row=row+4, column=0, padx=5, columnspan=9, pady=5, sticky="ew")

    ######################## vision distance ###############################
    vd_var = tk.StringVar()
    vd_options = {
        "s/c": "s/c",
        "c/c": "c/c"
    }

    vd_disabled_radiobuttons = False
    if record_data: 
        vd_data = record_data["VisionDistance"]
        vd_var.set(vd_data[1])
        vd_disabled_radiobuttons = True
        vd_od_prefill = vd_data[2]
        vd_oi_prefill = vd_data[3]
    else: 
        vd_od_prefill = ""
        vd_oi_prefill = ""


    vd_radiobuttons = create_label_and_radiobuttons(content_frame, label_text="Visión distancia (dVA):", row=row+5, col_start=0, 
                                                    options=vd_options, variable=vd_var, disabled=vd_disabled_radiobuttons) # row, col_start, options, variable
    vd_validate_command = content_frame.register(utils.validate_vision_distance_input) 
    vd_entry_od, vd_entry_od_label = create_label_and_entry(content_frame, "OD:", row+6, 0, 1, "20/", vd_od_prefill) # row, col_start, colspan_label, colspan_entry
    vd_entry_od.config(validate="key", validatecommand=(vd_validate_command, "%P"))
    vd_entry_oi, vd_entry_oi_label = create_label_and_entry(content_frame, "OI:", row+7, 0, 1, "20/", vd_oi_prefill)
    vd_entry_oi.config(validate="key", validatecommand=(vd_validate_command, "%P"))

    ######################## dilatation ###############################
    dilatation_var = tk.IntVar()
    dilatation_timestamp_var = tk.StringVar()
    dilatation_checkbox_text = "Dilatación"
    if record_data: 
        dilatation_data = record_data["Dilatation"]
        dilatation_var.set(dilatation_data[1])
        if dilatation_data[1] == 1: 
            dilatation_checkbox_text = f"Dilatación @ tiempo {dilatation_data[2]}"

    dilatation_checkbox = tk.Checkbutton(content_frame, text=dilatation_checkbox_text, variable=dilatation_var, state="disabled" if record_data else "normal")
    dilatation_checkbox.config(command=lambda checkbox_text="Dilatación", timestamp_var=dilatation_timestamp_var, checkbox_var=dilatation_var, checkbox=dilatation_checkbox: 
                               utils.update_checkbox_timestamp(timestamp_var, checkbox, checkbox_var, checkbox_text))
    dilatation_checkbox.grid(row=row+5, column=4, columnspan=2, padx=5, pady=5, sticky="w")

    separator_2 = ttk.Separator(content_frame, orient='horizontal')
    separator_2.grid(row=row+8, column=0, padx=5, columnspan=9, pady=5, sticky="ew")

    ######################## intraocular pressure ###############################
    ip_widgets = [] 
    count = 1
    row += 9

    def push_widgets_down(): 
        # push rest of the form down 
        separator_3.grid(row=row+3, column=0, padx=5, columnspan=9, pady=5, sticky="ew")

        for idx, rs_radiobutton in enumerate(rs_radiobuttons):
            rs_radiobutton.grid(row=row+4, column=idx, padx=10, pady=5, sticky="w")
        for idx, rs_label in enumerate(rs_col_labels):
            rs_label.grid(row=row+5, column=1+idx, padx=10, pady=5, sticky="w")
        for idx, rs_label in enumerate(rs_row_labels):
            rs_label.grid(row=row+6+idx, column=0, padx=10, pady=5, sticky="w")
        for idx, rs_entry in enumerate(rs_entries):
            rs_entry.grid(row=row+6+(idx//3), column=1+(idx%3), padx=10, pady=5, sticky="w")
        separator_4.grid(row=row+8, column=0, padx=5, columnspan=9, pady=5, sticky="ew")

        gp_title.grid(row=row+9, column=0, columnspan=3, padx=10, pady=5, sticky="w")
        for idx, gp_label in enumerate(gp_col_labels):
            gp_label.grid(row=row+10, column=1+idx, padx=10, pady=5, sticky="w")
        for idx, gp_label in enumerate(gp_row_labels):
            gp_label.grid(row=row+11+idx, column=0, padx=10, pady=5, sticky="w")
        for idx, gp_entry in enumerate(gp_entries):
            gp_entry.grid(row=row+11+(idx//4), column=1+(idx%4), padx=10, pady=5, sticky="w")
        gp_pd_entry.grid(row=row+13, column=1, padx=10, pady=5, sticky="w")
        gp_pd_label.grid(row=row+13, column=2, padx=0, pady=5, sticky="w")
        separator_5.grid(row=row+14, column=0, padx=5, columnspan=9, pady=5, sticky="ew")

        table_labels[0].grid(row=row+15, column=0, columnspan=3, sticky="e", padx=130)
        table_labels[1].grid(row=row+15, column=4, columnspan=3, sticky="w", padx=150)
        for idx, table_entry in enumerate(table_entries):
            if idx == 6: 
                table_entry[0].grid(row=row+28, column=0, columnspan=3, padx=10, pady=5, sticky="e")
                table_entry[1].grid(row=row+28, column=3, padx=5, pady=2)
                table_entry[2].grid(row=row+28, column=4, columnspan=3, padx=10, pady=5, sticky="w")
            else: 
                for i, buttons in enumerate(table_entry[0]):
                    buttons.grid(row=row+16+idx*2, column=1+i, padx=10, pady=5, sticky="e")
                for i, buttons in enumerate(table_entry[1]):
                    buttons.grid(row=row+16+idx*2, column=4+i, padx=10, pady=5, sticky="w")
                table_entry[2].grid(row=row+16+idx*2, column=3, padx=5, pady=2)
                table_entry[3].grid(row=row+17+idx*2, column=0, columnspan=3, padx=10, pady=5, sticky="e")
                table_entry[4].grid(row=row+17+idx*2, column=4, columnspan=3, padx=10, pady=5, sticky="w")

        separator_6.grid(row=row+40, column=0, padx=5, columnspan=9, pady=5, sticky="ew")

        dx_label.grid(row=row+41, column=0, padx=10, pady=5, sticky="w")
        dx_myopia_checkbox.grid(row=row+41, column=1, padx=10, pady=5, sticky="w")
        dx_hyperopia_checkbox.grid(row=row+41, column=2, padx=10, pady=5, sticky="w")
        dx_astigmatism_checkbox.grid(row=row+41, column=3, padx=10, pady=5, sticky="w")
        dx_comments.grid(row=row+42, column=1, columnspan=6, padx=10, pady=5, sticky="w")
        tx_comments_label.grid(row=row+43, column=0, padx=10, pady=5, sticky="w")
        tx_comments.grid(row=row+43, column=1, columnspan=6, padx=10, pady=5, sticky="w")

        doctor_firstname_label.grid(row=row+44, column=0, padx=10, pady=5, sticky="w")
        doctor_firstname_entry.grid(row=row+44, column=1, padx=10, pady=5, sticky="w")
        doctor_lastname_label.grid(row=row+44, column=2, padx=10, pady=5, sticky="w")
        doctor_lastname_entry.grid(row=row+44, column=3, padx=10, pady=5, sticky="w")
        date_label.grid(row=row+44, column=5, padx=10, pady=5, sticky="w")


        save_button.grid(row=row+70, column=0, columnspan=7, padx=10, pady=10)

    def add_section(d=None):
        nonlocal count
        nonlocal row
        count += 1
        row += 3
        ip_widgets.append(create_intraocular_pressure_section(content_frame, count, row, d))
        if not record_data: 
            push_widgets_down()

    if record_data: 
        count = 0
        ip_data = record_data["IntraocularPressure"]
        for d in ip_data: 
            add_section(d)
    else: 
        ip_widgets.append(create_intraocular_pressure_section(content_frame, count, row))
        add_button = tk.Button(content_frame, text="Agregar nuevo", command=lambda: add_section(), state="disabled" if record_data else "normal")
        add_button.grid(row=row, column=5, padx=10, pady=10, sticky="w")

    separator_3 = ttk.Separator(content_frame, orient='horizontal')
    separator_3.grid(row=row+3, column=0, padx=5, columnspan=9, pady=5, sticky="we")

    ######################## refractive status ###############################
    rs_var = tk.StringVar()
    rs_options = {
        "Autorefraction": "Autorefraction",
        "Retinoscopia": "Retinoscopia"
    }

    rs_disabled_radiobuttons = False
    if record_data: 
        rs_data = record_data["RefractiveStatus"]
        rs_var.set(rs_data[1])
        rs_disabled_radiobuttons = True

    rs_radiobuttons = create_label_and_radiobuttons(content_frame, row=row+4, col_start=0, options=rs_options, variable=rs_var, disabled=rs_disabled_radiobuttons)
    rs_col_labels, rs_row_labels = create_table(content_frame, row+5, 0, ["OD:", "OI:"], ["Esfera", "Cilindro", "Eje"])
    rs_entries = []
    rs_sphere_od_entry = tk.Entry(content_frame)
    rs_sphere_od_entry.grid(row=row+6, column=1, padx=10, pady=5, sticky="w")
    rs_entries.append(rs_sphere_od_entry)
    rs_cylinder_od_entry = tk.Entry(content_frame)
    rs_cylinder_od_entry.grid(row=row+6, column=2, padx=10, pady=5, sticky="w")
    rs_entries.append(rs_cylinder_od_entry)
    rs_axis_od_entry = tk.Entry(content_frame)
    rs_axis_od_entry.grid(row=row+6, column=3, padx=10, pady=5, sticky="w")
    rs_entries.append(rs_axis_od_entry)

    rs_sphere_oi_entry = tk.Entry(content_frame)
    rs_sphere_oi_entry.grid(row=row+7, column=1, padx=10, pady=5, sticky="w")
    rs_entries.append(rs_sphere_oi_entry)
    rs_cylinder_oi_entry = tk.Entry(content_frame)
    rs_cylinder_oi_entry.grid(row=row+7, column=2, padx=10, pady=5, sticky="w")
    rs_entries.append(rs_cylinder_oi_entry)
    rs_axis_oi_entry = tk.Entry(content_frame)
    rs_axis_oi_entry.grid(row=row+7, column=3, padx=10, pady=5, sticky="w")
    rs_entries.append(rs_axis_oi_entry)

    if record_data: 
        rs_sphere_od_entry.insert(0, rs_data[2])
        rs_sphere_od_entry.config(state="readonly")
        rs_sphere_oi_entry.insert(0, rs_data[3])
        rs_sphere_oi_entry.config(state="readonly")
        rs_cylinder_od_entry.insert(0, rs_data[4])
        rs_cylinder_od_entry.config(state="readonly")
        rs_cylinder_oi_entry.insert(0, rs_data[5])
        rs_cylinder_oi_entry.config(state="readonly")
        rs_axis_od_entry.insert(0, rs_data[6])
        rs_axis_od_entry.config(state="readonly")
        rs_axis_oi_entry.insert(0, rs_data[7])
        rs_axis_oi_entry.config(state="readonly")

    separator_4 = ttk.Separator(content_frame, orient='horizontal')
    separator_4.grid(row=row+8, column=0, padx=5, columnspan=9, pady=5, sticky="ew")

    ######################## glasses prescription ###############################
    gp_title = tk.Label(content_frame, text="Rx de anteojos")
    gp_title.grid(row=row+9, column=0, columnspan=3, padx=10, pady=5, sticky="w")
    gp_col_labels, gp_row_labels = create_table(content_frame, row+10, 0, ["OD:", "OI:", "PD:"], ["Esfera", "Cilindro", "Eje", "dVA"])
    gp_entries = []
    gp_sphere_od_entry = tk.Entry(content_frame)
    gp_sphere_od_entry.grid(row=row+11, column=1, padx=10, pady=5, sticky="w")
    gp_entries.append(gp_sphere_od_entry)
    gp_cylinder_od_entry = tk.Entry(content_frame)
    gp_cylinder_od_entry.grid(row=row+11, column=2, padx=10, pady=5, sticky="w")
    gp_entries.append(gp_cylinder_od_entry)
    gp_axis_od_entry = tk.Entry(content_frame)
    gp_axis_od_entry.grid(row=row+11, column=3, padx=10, pady=5, sticky="w")
    gp_entries.append(gp_axis_od_entry)
    gp_dva_od_entry = tk.Entry(content_frame)
    gp_dva_od_entry.grid(row=row+11, column=4, padx=10, pady=5, sticky="w")
    gp_entries.append(gp_dva_od_entry)

    gp_sphere_oi_entry = tk.Entry(content_frame)
    gp_sphere_oi_entry.grid(row=row+12, column=1, padx=10, pady=5, sticky="w")
    gp_entries.append(gp_sphere_oi_entry)
    gp_cylinder_oi_entry = tk.Entry(content_frame)
    gp_cylinder_oi_entry.grid(row=row+12, column=2, padx=10, pady=5, sticky="w")
    gp_entries.append(gp_cylinder_oi_entry)
    gp_axis_oi_entry = tk.Entry(content_frame)
    gp_axis_oi_entry.grid(row=row+12, column=3, padx=10, pady=5, sticky="w")
    gp_entries.append(gp_axis_oi_entry)
    gp_dva_oi_entry = tk.Entry(content_frame)
    gp_dva_oi_entry.grid(row=row+12, column=4, padx=10, pady=5, sticky="w")
    gp_entries.append(gp_dva_oi_entry)

    gp_pd_entry = tk.Entry(content_frame)
    gp_pd_entry.grid(row=row+13, column=1, padx=10, pady=5, sticky="w")
    gp_pd_label = tk.Label(content_frame, text="mm")
    gp_pd_label.grid(row=row+13, column=2, padx=0, pady=5, sticky="w")

    if record_data: 
        gp_data = record_data["GlassesPrescription"]
        gp_sphere_od_entry.insert(0, gp_data[1])
        gp_sphere_od_entry.config(state="readonly")
        gp_sphere_oi_entry.insert(0, gp_data[2])
        gp_sphere_oi_entry.config(state="readonly")
        gp_cylinder_od_entry.insert(0, gp_data[3])
        gp_cylinder_od_entry.config(state="readonly")
        gp_cylinder_oi_entry.insert(0, gp_data[4])
        gp_cylinder_oi_entry.config(state="readonly")
        gp_axis_od_entry.insert(0, gp_data[5])
        gp_axis_od_entry.config(state="readonly")
        gp_axis_oi_entry.insert(0, gp_data[6])
        gp_axis_oi_entry.config(state="readonly")
        gp_dva_od_entry.insert(0, gp_data[7])
        gp_dva_od_entry.config(state="readonly")
        gp_dva_oi_entry.insert(0, gp_data[8])
        gp_dva_oi_entry.config(state="readonly")
        gp_pd_entry.insert(0, gp_data[9])
        gp_pd_entry.config(state="readonly")

    separator_5 = ttk.Separator(content_frame, orient='horizontal')
    separator_5.grid(row=row+14, column=0, padx=5, columnspan=9, pady=5, sticky="ew")

    ######################## table ###############################
    od_frame = tk.Frame(content_frame)
    od_frame.grid(row=row+15, column=0, columnspan=3, sticky="e", padx=80)
    table_od_label = tk.Label(od_frame, text="OD", font=("Helvetica", 10, "bold"))
    table_od_label.pack(side="left", padx=(0, 5))

    def update_all_normal(var): 
        var.set("1")

    od_all_normal = tk.IntVar()
    od_all_normal_checkbox = tk.Button(od_frame, text="Todo normal", command=lambda var=od_all_normal: update_all_normal(var))
    od_all_normal_checkbox.pack(side="left")

    oi_frame = tk.Frame(content_frame)
    oi_frame.grid(row=row+15, column=4, columnspan=3, sticky="w", padx=80)
    table_oi_label = tk.Label(oi_frame, text="OI", font=("Helvetica", 10, "bold"))
    table_oi_label.pack(side="left", padx=(0, 5))
    oi_all_normal = tk.IntVar()
    oi_all_normal_checkbox = tk.Button(oi_frame, text="Todo normal", command=lambda var=oi_all_normal: update_all_normal(var))
    oi_all_normal_checkbox.pack(side="left")

    table_labels = [od_frame, oi_frame]

    table_entries = []

    if record_data:
        table_data = record_data["OcularAssessmentTable"]
    
    ###############################################################################

    eyelid_od_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)
    eyelid_oi_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)

    if record_data: 
        eyelid_od_prefill = table_data[1]
        eyelid_oi_prefill = table_data[3]
        if table_data[2]: 
            eyelid_od_comment.insert("1.0", table_data[2]) 
        if table_data[4]: 
            eyelid_oi_comment.insert("1.0", table_data[4]) 
    else: 
        eyelid_od_prefill = eyelid_oi_prefill = None

    eyelid_od_var, eyelid_oi_var, eyelid_od_radiobuttons, eyelid_oi_radiobuttons, eyelid_label = create_row(
        content_frame, "Párpados", eyelid_od_comment, eyelid_oi_comment, row+16, od_all_normal, oi_all_normal,
        status="disabled" if record_data else "normal", od_data=eyelid_od_prefill, oi_data=eyelid_oi_prefill)
    eyelid_widgets = [eyelid_od_radiobuttons, eyelid_oi_radiobuttons, eyelid_label, eyelid_od_comment, eyelid_oi_comment]
    table_entries.append(eyelid_widgets)

    ###############################################################################

    conjunctiva_od_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)
    conjunctiva_oi_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)

    if record_data: 
        conjunctiva_od_prefill = table_data[5]
        conjunctiva_oi_prefill = table_data[7]
        if table_data[6]: 
            conjunctiva_od_comment.insert("1.0", table_data[6]) 
        if table_data[8]: 
            conjunctiva_oi_comment.insert("1.0", table_data[8]) 
    else: 
        conjunctiva_od_prefill = conjunctiva_oi_prefill = None

    conjunctiva_od_var, conjunctiva_oi_var, conjunctiva_od_radiobuttons, conjunctiva_oi_radiobuttons, conjunctiva_label = create_row(
        content_frame, "Conjunctiva", conjunctiva_od_comment, conjunctiva_oi_comment, row+18, od_all_normal, oi_all_normal,
        status="disabled" if record_data else "normal", od_data=conjunctiva_od_prefill, oi_data=conjunctiva_oi_prefill)
    conjunctiva_widgets = [conjunctiva_od_radiobuttons, conjunctiva_oi_radiobuttons, conjunctiva_label, conjunctiva_od_comment, conjunctiva_oi_comment]
    table_entries.append(conjunctiva_widgets)

    ###############################################################################

    cornea_od_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)
    cornea_oi_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)

    if record_data: 
        cornea_od_prefill = table_data[9]
        cornea_oi_prefill = table_data[11]
        if table_data[10]: 
            cornea_od_comment.insert("1.0", table_data[10]) 
        if table_data[12]: 
            cornea_oi_comment.insert("1.0", table_data[12]) 
    else: 
        cornea_od_prefill = cornea_oi_prefill = None

    cornea_od_var, cornea_oi_var, cornea_od_radiobuttons, cornea_oi_radiobuttons, cornea_label = create_row(
        content_frame, "Cornea", cornea_od_comment, cornea_oi_comment, row+20, od_all_normal, oi_all_normal,
        status="disabled" if record_data else "normal", od_data=cornea_od_prefill, oi_data=cornea_oi_prefill)
    cornea_widgets = [cornea_od_radiobuttons, cornea_oi_radiobuttons, cornea_label, cornea_od_comment, cornea_oi_comment]
    table_entries.append(cornea_widgets)

    ###############################################################################

    iris_od_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)
    iris_oi_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)

    if record_data: 
        iris_od_prefill = table_data[13]
        iris_oi_prefill = table_data[15]
        if table_data[14]: 
            iris_od_comment.insert("1.0", table_data[14]) 
        if table_data[16]: 
            iris_oi_comment.insert("1.0", table_data[16]) 
    else: 
        iris_od_prefill = iris_oi_prefill = None

    iris_od_var, iris_oi_var, iris_od_radiobuttons, iris_oi_radiobuttons, iris_label = create_row(
        content_frame, "Iris", iris_od_comment, iris_oi_comment, row+22, od_all_normal, oi_all_normal,
        status="disabled" if record_data else "normal", od_data=iris_od_prefill, oi_data=iris_oi_prefill)
    iris_widgets = [iris_od_radiobuttons, iris_oi_radiobuttons, iris_label, iris_od_comment, iris_oi_comment]
    table_entries.append(iris_widgets)

    ###############################################################################

    pupil_od_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)
    pupil_oi_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)

    if record_data: 
        pupil_od_prefill = table_data[17]
        pupil_oi_prefill = table_data[19]
        if table_data[18]: 
            pupil_od_comment.insert("1.0", table_data[18]) 
        if table_data[20]: 
            pupil_oi_comment.insert("1.0", table_data[20]) 
    else: 
        pupil_od_prefill = pupil_oi_prefill = None

    pupil_od_var, pupil_oi_var, pupil_od_radiobuttons, pupil_oi_radiobuttons, pupil_label = create_row(
        content_frame, "Pupil", pupil_od_comment, pupil_oi_comment, row+24, od_all_normal, oi_all_normal,
        status="disabled" if record_data else "normal", od_data=pupil_od_prefill, oi_data=pupil_oi_prefill)
    pupil_widgets = [pupil_od_radiobuttons, pupil_oi_radiobuttons, pupil_label, pupil_od_comment, pupil_oi_comment]
    table_entries.append(pupil_widgets)

    ###############################################################################

    lente_od_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)
    lente_oi_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)

    if record_data: 
        lente_od_prefill = table_data[21]
        lente_oi_prefill = table_data[23]
        if table_data[22]: 
            lente_od_comment.insert("1.0", table_data[22]) 
        if table_data[24]: 
            lente_oi_comment.insert("1.0", table_data[24]) 
    else: 
        lente_od_prefill = lente_oi_prefill = None

    lente_od_var, lente_oi_var, lente_od_radiobuttons, lente_oi_radiobuttons, lente_label = create_row(
        content_frame, "Lente", lente_od_comment, lente_oi_comment, row+26, od_all_normal, oi_all_normal,
        status="disabled" if record_data else "normal", od_data=lente_od_prefill, oi_data=lente_oi_prefill)
    lente_widgets = [lente_od_radiobuttons, lente_oi_radiobuttons, lente_label, lente_od_comment, lente_oi_comment]
    table_entries.append(lente_widgets)

    ###############################################################################

    cd_od_entry = tk.Entry(content_frame, width=30)
    cd_od_entry.grid(row=row+28, column=0, columnspan=3, padx=10, pady=5, sticky="e")
    cd_label = tk.Label(content_frame, text="C/D")
    cd_label.grid(row=row+28, column=3, padx=5, pady=2)
    cd_oi_entry = tk.Entry(content_frame, width=30)
    cd_oi_entry.grid(row=row+28, column=4, columnspan=3, padx=10, pady=5, sticky="w")

    if record_data: 
        cd_od_entry.insert(0, table_data[25])
        cd_od_entry.config(state="readonly")
        cd_oi_entry.insert(0, table_data[26])
        cd_oi_entry.config(state="readonly")

    cd_widgets = [cd_od_entry, cd_label, cd_oi_entry]
    table_entries.append(cd_widgets)

    ###############################################################################

    nerve_od_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)
    nerve_oi_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)

    if record_data: 
        nerve_od_prefill = table_data[27]
        nerve_oi_prefill = table_data[29]
        if table_data[28]: 
            nerve_od_comment.insert("1.0", table_data[28]) 
        if table_data[30]: 
            nerve_oi_comment.insert("1.0", table_data[30]) 
    else: 
        nerve_od_prefill = nerve_oi_prefill = None

    nerve_od_var, nerve_oi_var, nerve_od_radiobuttons, nerve_oi_radiobuttons, nerve_label = create_row(
        content_frame, "Nervio", nerve_od_comment, nerve_oi_comment, row+29, od_all_normal, oi_all_normal,
        status="disabled" if record_data else "normal", od_data=nerve_od_prefill, oi_data=nerve_oi_prefill)
    nerve_widgets = [nerve_od_radiobuttons, nerve_oi_radiobuttons, nerve_label, nerve_od_comment, nerve_oi_comment]
    table_entries.append(nerve_widgets)

    ###############################################################################

    macula_od_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)
    macula_oi_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)

    if record_data: 
        macula_od_prefill = table_data[31]
        macula_oi_prefill = table_data[33]
        if table_data[32]: 
            macula_od_comment.insert("1.0", table_data[32]) 
        if table_data[34]: 
            macula_oi_comment.insert("1.0", table_data[34]) 
    else: 
        macula_od_prefill = macula_oi_prefill = None

    macula_od_var, macula_oi_var, macula_od_radiobuttons, macula_oi_radiobuttons, macula_label = create_row(
        content_frame, "Macula", macula_od_comment, macula_oi_comment, row+31, od_all_normal, oi_all_normal,
        status="disabled" if record_data else "normal", od_data=macula_od_prefill, oi_data=macula_oi_prefill)
    macula_widgets = [macula_od_radiobuttons, macula_oi_radiobuttons, macula_label, macula_od_comment, macula_oi_comment]
    table_entries.append(macula_widgets)

    ###############################################################################

    vasculature_od_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)
    vasculature_oi_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)

    if record_data: 
        vasculature_od_prefill = table_data[35]
        vasculature_oi_prefill = table_data[37]
        if table_data[36]: 
            vasculature_od_comment.insert("1.0", table_data[36]) 
        if table_data[38]: 
            vasculature_oi_comment.insert("1.0", table_data[38]) 
    else: 
        vasculature_od_prefill = vasculature_oi_prefill = None

    vasculature_od_var, vasculature_oi_var, vasculature_od_radiobuttons, vasculature_oi_radiobuttons, vasculature_label = create_row(
        content_frame, "Vasculatura", vasculature_od_comment, vasculature_oi_comment, row+33, od_all_normal, oi_all_normal,
        status="disabled" if record_data else "normal", od_data=vasculature_od_prefill, oi_data=vasculature_oi_prefill)
    vasculature_widgets = [vasculature_od_radiobuttons, vasculature_oi_radiobuttons, vasculature_label, vasculature_od_comment, vasculature_oi_comment]
    table_entries.append(vasculature_widgets)

    ###############################################################################

    periphery_od_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)
    periphery_oi_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)

    if record_data: 
        periphery_od_prefill = table_data[39]
        periphery_oi_prefill = table_data[41]
        if table_data[40]: 
            periphery_od_comment.insert("1.0", table_data[40]) 
        if table_data[42]: 
            periphery_oi_comment.insert("1.0", table_data[42]) 
    else: 
        periphery_od_prefill = periphery_oi_prefill = None

    periphery_od_var, periphery_oi_var, periphery_od_radiobuttons, periphery_oi_radiobuttons, periphery_label = create_row(
        content_frame, "Periferia", periphery_od_comment, periphery_oi_comment, row+35, od_all_normal, oi_all_normal,
        status="disabled" if record_data else "normal", od_data=periphery_od_prefill, oi_data=periphery_oi_prefill)
    periphery_widgets = [periphery_od_radiobuttons, periphery_oi_radiobuttons, periphery_label, periphery_od_comment, periphery_oi_comment]
    table_entries.append(periphery_widgets)

    ###############################################################################

    vitreous_od_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)
    vitreous_oi_comment = tk.Text(content_frame, height=3, bg="lightgray", width=60)

    if record_data: 
        vitreous_od_prefill = table_data[43]
        vitreous_oi_prefill = table_data[45]
        if table_data[44]: 
            vitreous_od_comment.insert("1.0", table_data[44]) 
        if table_data[46]: 
            vitreous_oi_comment.insert("1.0", table_data[46]) 
    else: 
        vitreous_od_prefill = vitreous_oi_prefill = None

    vitreous_od_var, vitreous_oi_var, vitreous_od_radiobuttons, vitreous_oi_radiobuttons, vitreous_label = create_row(
        content_frame, "Vitreous", vitreous_od_comment, vitreous_oi_comment, row+37, od_all_normal, oi_all_normal,
        status="disabled" if record_data else "normal", od_data=vitreous_od_prefill, oi_data=vitreous_oi_prefill)
    vitreous_widgets = [vitreous_od_radiobuttons, vitreous_oi_radiobuttons, vitreous_label, vitreous_od_comment, vitreous_oi_comment]
    table_entries.append(vitreous_widgets)

    ###############################################################################

    separator_6 = ttk.Separator(content_frame, orient='horizontal')
    separator_6.grid(row=row+39, column=0, padx=5, columnspan=9, pady=5, sticky="ew")

    ######################## diagnosis ###############################
    dx_label = tk.Label(content_frame, text="Dx:")
    dx_label.grid(row=row+40, column=0, sticky="w", padx=10, pady=5)
    dx_myopia_var = tk.IntVar()
    dx_myopia_checkbox = tk.Checkbutton(content_frame, text="Miopía", variable=dx_myopia_var)
    dx_myopia_checkbox.grid(row=row+40, column=1, padx=5, pady=5, sticky="w")
    dx_hyperopia_var = tk.IntVar()
    dx_hyperopia_checkbox = tk.Checkbutton(content_frame, text="Hipermetropía", variable=dx_hyperopia_var)
    dx_hyperopia_checkbox.grid(row=row+40, column=2, padx=5, pady=5, sticky="w")
    dx_astigmatism_var = tk.IntVar()
    dx_astigmatism_checkbox = tk.Checkbutton(content_frame, text="Astigmatismo", variable=dx_astigmatism_var)
    dx_astigmatism_checkbox.grid(row=row+40, column=3, padx=5, pady=5, sticky="w")

    if record_data:
        diagnosis_data = record_data["Diagnosis"]
        dx_myopia_var.set(diagnosis_data[1])
        dx_myopia_checkbox.config(state="disabled")
        dx_hyperopia_var.set(diagnosis_data[2])
        dx_hyperopia_checkbox.config(state="disabled")
        dx_astigmatism_var.set(diagnosis_data[3])
        dx_astigmatism_checkbox.config(state="disabled")
        dx_comments_prefill = diagnosis_data[4]
        tx_comments_prefill = diagnosis_data[5]
    else: 
        dx_comments_prefill = tx_comments_prefill = ""

    dx_comments, dx_comments_label = create_label_and_text(content_frame, row+41, 7, width=100, prefill_value=dx_comments_prefill) 
    tx_comments, tx_comments_label = create_label_and_text(content_frame, row+42, 7, label_text="Tx:", width=100, prefill_value=tx_comments_prefill)

    row = row+43

    if record_data: 
        doctor_data = record_data["Doctor"]
        doctor_firstname_prefill = doctor_data[2]
        doctor_lastname_prefill = doctor_data[3]
        creation_date_prefill = record_data["CreatedAt"]
        last_edit_date_prefill = record_data["LastEditedAt"]
        date_label = tk.Label(content_frame, text=f"Hecho en {creation_date_prefill}")
        date_label.grid(row=row, column=5, padx=10, pady=5, sticky="w")
        date_label = tk.Label(content_frame, text=f"Última revisión {last_edit_date_prefill}")
        date_label.grid(row=row+1, column=5, padx=10, pady=5, sticky="w")
    else: 
        doctor_firstname_prefill = doctor_lastname_prefill = None
        date_label = tk.Label(content_frame, text=f"Fecha: {creation_date}")
        date_label.grid(row=row, column=5, padx=10, pady=5, sticky="w")

    doctor_firstname_entry, doctor_firstname_label = create_label_and_entry(content_frame, "Nombre de Doctor:", row, 0, 1, prefill_value=doctor_firstname_prefill) 
    doctor_lastname_entry, doctor_lastname_label = create_label_and_entry(content_frame, "Apellido de Doctor:", row, 2, 1, prefill_value=doctor_lastname_prefill)

    ######################## addendum ###############################
    row += 2

    if record_data:
        separator_7 = ttk.Separator(content_frame, orient='horizontal')
        separator_7.grid(row=row, column=0, padx=5, columnspan=9, pady=5, sticky="ew")
        addendum_data = record_data["Addendum"]
        if addendum_data:
            for idx, addendum in enumerate(addendum_data):
                addendum_text = addendum[1]
                addendum_date = utils.format_date(addendum[2])
                addendum_doctor_row = db.fetch_row(cur, "Doctor", "DoctorID", addendum[4])
                addendum_doctor_name = " ".join([addendum_doctor_row[2], addendum_doctor_row[3]])
                tk.Label(content_frame, text=f"#{idx+1}").grid(row=row+1, column=0, padx=10, pady=5, sticky="w")
                tk.Label(content_frame, text=f"Fecha: {addendum_date}").grid(row=row+1, column=1, padx=10, pady=5, sticky="w")
                tk.Label(content_frame, text=f"Doctor: {addendum_doctor_name}").grid(row=row+1, column=2, padx=10, pady=5, sticky="w")
                tk.Label(content_frame, text=f"Texto: {addendum_text}", wraplength=800, justify="left").grid(
                    row=row+1, column=3, columnspan=4, padx=10, pady=5, sticky="w")
                row += 1
        addendum_entry, addendum_label = create_label_and_text(content_frame, row+1, 7, label_text="Apéndice:", width=100)
        row += 2

        addendum_doctor_firstname_entry, addendum_doctor_firstname_label = create_label_and_entry(content_frame, "Nombre de Doctor:", row, 0, 1) 
        addendum_doctor_lastname_entry, addendum_doctor_lastname_label = create_label_and_entry(content_frame, "Apellido de Doctor:", row, 2, 1)
        addendum_date_label = tk.Label(content_frame, text=f"Fecha: {creation_date}")
        addendum_date_label.grid(row=row, column=5, padx=10, pady=5, sticky="w")
        row += 1

    ######################## save ###############################
    def on_save(): 
        if record_data: 
            record_id = record_data["RecordID"]
            addendum = addendum_entry.get("1.0", tk.END).strip()
            if len(addendum) > 0: 
                addendum_doctor_firstname = addendum_doctor_firstname_entry.get()
                addendum_doctor_lastname = addendum_doctor_lastname_entry.get()
                addendum_doctor_id = utils.generate_id(addendum_doctor_firstname, addendum_doctor_lastname)

                doctor_row = db.fetch_row(cur, "Doctor", "DoctorID", addendum_doctor_id)
                if not doctor_row:
                    db.insert_doctor(cur, addendum_doctor_id, addendum_doctor_firstname, addendum_doctor_lastname)
                
                current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                db.insert_addendum(cur, current_time, addendum, record_id, addendum_doctor_id)
                db.update_record_last_edit_time(cur, record_id, current_time)
        else: 
            school = school_entry.get()
            firstname = firstname_entry.get()
            lastname = lastname_entry.get()
            dob = dob_entry.get()
            phone_number = phone_number_entry.get()
            reason_for_visit = reason_for_visit_entry.get("1.0", tk.END) 

            student_id = utils.generate_id(firstname, lastname, dob)

            vd_method = vd_var.get()
            vd_od = vd_entry_od.get()
            vd_oi = vd_entry_oi.get()

            dilatation = dilatation_var.get()
            dilatation_timestamp = dilatation_timestamp_var.get()

            rs_method = rs_var.get()
            rs_sphere_od = rs_sphere_od_entry.get()
            rs_cylinder_od = rs_cylinder_od_entry.get()
            rs_axis_od = rs_axis_od_entry.get()
            rs_sphere_oi = rs_sphere_oi_entry.get()
            rs_cylinder_oi = rs_cylinder_oi_entry.get()
            rs_axis_oi = rs_axis_oi_entry.get()

            gs_sphere_od = gp_sphere_od_entry.get()
            gs_cylinder_od = gp_cylinder_od_entry.get()
            gs_axis_od = gp_axis_od_entry.get()
            gs_dva_od = gp_dva_od_entry.get()
            gs_sphere_oi = gp_sphere_oi_entry.get()
            gs_cylinder_oi = gp_cylinder_oi_entry.get()
            gs_axis_oi = gp_axis_oi_entry.get()
            gs_dva_oi = gp_dva_oi_entry.get()
            gs_pd = gp_pd_entry.get()

            eyelid_od = eyelid_od_var.get()
            eyelid_oi = eyelid_oi_var.get()
            eyelid_od_cmt = eyelid_od_comment.get("1.0", tk.END)
            eyelid_oi_cmt = eyelid_oi_comment.get("1.0", tk.END)
            conjunctiva_od = conjunctiva_od_var.get()
            conjunctiva_oi = conjunctiva_oi_var.get()
            conjunctiva_od_cmt = conjunctiva_od_comment.get("1.0", tk.END)
            conjunctiva_oi_cmt = conjunctiva_oi_comment.get("1.0", tk.END)
            cornea_od = cornea_od_var.get()
            cornea_oi = cornea_oi_var.get()
            cornea_od_cmt = cornea_od_comment.get("1.0", tk.END)
            cornea_oi_cmt = cornea_oi_comment.get("1.0", tk.END)
            iris_od = iris_od_var.get()
            iris_oi = iris_oi_var.get()
            iris_od_cmt = iris_od_comment.get("1.0", tk.END)
            iris_oi_cmt = iris_oi_comment.get("1.0", tk.END)
            pupil_od = pupil_od_var.get()
            pupil_oi = pupil_oi_var.get()
            pupil_od_cmt = pupil_od_comment.get("1.0", tk.END)
            pupil_oi_cmt = pupil_oi_comment.get("1.0", tk.END)
            lente_od = lente_od_var.get()
            lente_oi = lente_oi_var.get()
            lente_od_cmt = lente_od_comment.get("1.0", tk.END)
            lente_oi_cmt = lente_oi_comment.get("1.0", tk.END)
            cd_od = cd_od_entry.get()
            cd_oi = cd_oi_entry.get()
            nerve_od = nerve_od_var.get()
            nerve_oi = nerve_oi_var.get()
            nerve_od_cmt = nerve_od_comment.get("1.0", tk.END)
            nerve_oi_cmt = nerve_oi_comment.get("1.0", tk.END)
            macula_od = macula_od_var.get()
            macula_oi = macula_oi_var.get()
            macula_od_cmt = macula_od_comment.get("1.0", tk.END)
            macula_oi_cmt = macula_oi_comment.get("1.0", tk.END)
            vasculature_od = vasculature_od_var.get()
            vasculature_oi = vasculature_oi_var.get()
            vasculature_od_cmt = vasculature_od_comment.get("1.0", tk.END)
            vasculature_oi_cmt = vasculature_oi_comment.get("1.0", tk.END)
            periphery_od = periphery_od_var.get()
            periphery_oi = periphery_oi_var.get()
            periphery_od_cmt = periphery_od_comment.get("1.0", tk.END)
            periphery_oi_cmt = periphery_oi_comment.get("1.0", tk.END)
            vitreous_od = vitreous_od_var.get()
            vitreous_oi = vitreous_oi_var.get()
            vitreous_od_cmt = vitreous_od_comment.get("1.0", tk.END)
            vitreous_oi_cmt = vitreous_oi_comment.get("1.0", tk.END)

            dx_myopia = dx_myopia_var.get()
            dx_hyperopia = dx_hyperopia_var.get()
            dx_astigmatism = dx_astigmatism_var.get()
            dx_comment = dx_comments.get("1.0", tk.END)
            tx_comment = tx_comments.get("1.0", tk.END)

            doctor_firstname = doctor_firstname_entry.get()
            doctor_lastname = doctor_lastname_entry.get()

            doctor_id = utils.generate_id(doctor_firstname, doctor_lastname)

            # Check for existing school and student
            school_row = db.fetch_row(cur, "School", "Name", school)
            if school_row:
                school_id = school_row[0]
            else:
                school_id = db.insert_school(cur, school)

            student_row = db.fetch_row(cur, "Student", "StudentID", student_id)
            if not student_row:
                db.insert_student(cur, student_id, firstname, lastname, dob, phone_number, school_id)
            
            doctor_row = db.fetch_row(cur, "Doctor", "DoctorID", doctor_id)
            if not doctor_row:
                db.insert_doctor(cur, doctor_id, doctor_firstname, doctor_lastname)

            # Insert exam record
            vd_id = db.insert_vision_distance(cur, vd_method, vd_od, vd_oi)
            dilatation_id = db.insert_dilatation(cur, dilatation, dilatation_timestamp)
            rs_id = db.insert_refractive_status(cur, rs_method, rs_sphere_od, rs_sphere_oi, rs_cylinder_od, rs_cylinder_oi, rs_axis_od, rs_axis_oi)
            gs_id = db.insert_glasses_prescription(cur, gs_sphere_od, gs_sphere_oi, gs_cylinder_od, gs_cylinder_oi, gs_axis_od, gs_axis_oi, gs_dva_od, gs_dva_oi, gs_pd)
            table_id = db.insert_ocular_assessment_table(cur, eyelid_od, eyelid_od_cmt, eyelid_oi, eyelid_oi_cmt, conjunctiva_od, conjunctiva_od_cmt, conjunctiva_oi, conjunctiva_oi_cmt, 
                                                        cornea_od, cornea_od_cmt, cornea_oi, cornea_oi_cmt, iris_od, iris_od_cmt, iris_oi, iris_oi_cmt, pupil_od, pupil_od_cmt, pupil_oi, pupil_oi_cmt,
                                                        lente_od, lente_od_cmt, lente_oi, lente_oi_cmt, cd_od, cd_oi, nerve_od, nerve_od_cmt, nerve_oi, nerve_oi_cmt, macula_od, macula_od_cmt, macula_oi, macula_oi_cmt,
                                                        vasculature_od, vasculature_od_cmt, vasculature_oi, vasculature_oi_cmt, periphery_od, periphery_od_cmt, periphery_oi, periphery_oi_cmt, vitreous_od, vitreous_od_cmt, vitreous_oi, vitreous_oi_cmt)
            diagnosis_id = db.insert_diagnosis(cur, dx_myopia, dx_hyperopia, dx_astigmatism, dx_comment, tx_comment)
            current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            record_id = db.insert_record(cur, creation_date, current_time, reason_for_visit, student_id, doctor_id, vd_id, dilatation_id, rs_id, gs_id, table_id, diagnosis_id)

            for ip in ip_widgets:
                ip_method = ip[0].get()
                ip_od = ip[2].get()
                ip_od_timestamp = ip[3].get()
                ip_oi = ip[4].get()
                ip_oi_timestamp = ip[5].get()
            
                db.insert_intraocular_pressure(cur, ip_method, ip_od, ip_od_timestamp, ip_oi, ip_oi_timestamp, record_id)

        messagebox.showinfo("Éxito", "Registro guardado exitosamente.")
        window.destroy() 

    if record_data: 
        save_button = tk.Button(content_frame, text="Guardar y Cerrar", command=lambda: on_save())
        save_button.grid(row=row+1, column=0, columnspan=3, pady=10, sticky="e")
        export_button = tk.Button(content_frame, text="Exportar", command=lambda: utils.export_to_pdf(record_data))
        export_button.grid(row=row+1, column=4, columnspan=3, pady=10, sticky="w")
    else:     
        save_button = tk.Button(content_frame, text="Guardar", command=lambda: on_save())
        save_button.grid(row=row+1, column=0, columnspan=7, pady=10)