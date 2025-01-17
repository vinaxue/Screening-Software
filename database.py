import sqlite3

import utils

def connect_database(): 
    con = sqlite3.connect("guatemalan_school_screening_data.db")
    cur = con.cursor()
    return cur

def create_tables(cur): 
    cur.execute('''CREATE TABLE IF NOT EXISTS School(
                Name VARCHAR(255) NOT NULL
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Student(
                StudentID VARCHAR(255) NOT NULL PRIMARY KEY,
                FirstName VARCHAR(255) NOT NULL CHECK(FirstName GLOB '[a-zA-Z]*'), 
                LastName VARCHAR(255) NOT NULL CHECK(LastName GLOB '[a-zA-Z]*'), 
                DateOfBirth DATE NOT NULL CHECK(DateOfBirth GLOB '__/__/____'), 
                PhoneNumber VARCHAR(255) NOT NULL CHECK(PhoneNumber GLOB '[0-9]*'), 
                SchoolID INTEGER NOT NULL,
                FOREIGN KEY (SchoolID) REFERENCES School(_rowid_)
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Doctor(
                DoctorID VARCHAR(255) NOT NULL PRIMARY KEY,
                FirstName VARCHAR(255) NOT NULL CHECK(FirstName GLOB '[a-zA-Z]*'), 
                LastName VARCHAR(255) NOT NULL CHECK(LastName GLOB '[a-zA-Z]*')
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS VisionDistance(
                VisionDistanceMethod TEXT NOT NULL CHECK(VisionDistanceMethod IN ('s/c', 'c/c')), 
                VisionDistanceOD FLOAT NOT NULL,
                VisionDistanceOI FLOAT NOT NULL
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS IntraocularPressure(
                IntraocularPressureMethod TEXT NOT NULL CHECK(IntraocularPressureMethod IN ('iCare', 'GAT')), 
                IntraocularPressureOD FLOAT NOT NULL, 
                IntraocularPressureODTimestamp TIMESTAMP,
                IntraocularPressureOI FLOAT NOT NULL, 
                IntraocularPressureOITimestamp TIMESTAMP,
                RecordID INTEGER NOT NULL, 
                FOREIGN KEY (RecordID) REFERENCES Record(_rowid_)
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Dilatation(
                Dilatation BIT,
                DilatationTimestamp TIMESTAMP NULL
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS RefractiveStatus(
                RefractiveStatusMethod TEXT NOT NULL CHECK(RefractiveStatusMethod IN ('Autorefraction', 'Retinoscopia')), 
                RefractiveStatusSphereOD FLOAT NOT NULL, 
                RefractiveStatusSphereOI FLOAT NOT NULL, 
                RefractiveStatusCylinderOD FLOAT NOT NULL, 
                RefractiveStatusCylinderOI FLOAT NOT NULL, 
                RefractiveStatusAxisOD FLOAT NOT NULL, 
                RefractiveStatusAxisOI FLOAT NOT NULL
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS GlassesPrescription(
                GlassesPrescriptionSphereOD FLOAT NOT NULL, 
                GlassesPrescriptionSphereOI FLOAT NOT NULL, 
                GlassesPrescriptionCylinderOD FLOAT NOT NULL, 
                GlassesPrescriptionCylinderOI FLOAT NOT NULL, 
                GlassesPrescriptionAxisOD FLOAT NOT NULL, 
                GlassesPrescriptionAxisOI FLOAT NOT NULL, 
                GlassesPrescriptionDvaOD FLOAT NOT NULL, 
                GlassesPrescriptionDvaOI FLOAT NOT NULL, 
                GlassesPrescriptionPD FLOAT NOT NULL
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS OcularAssessmentTable (
                EyelidOD CHECK(EyelidOD IN ('Normal', 'Anormal')) NOT NULL,
                EyelidCommentOD TEXT,
                EyelidOI CHECK(EyelidOI IN ('Normal', 'Anormal')) NOT NULL,
                EyelidCommentOI TEXT,
                
                ConjunctivaOD CHECK(ConjunctivaOD IN ('Normal', 'Anormal')) NOT NULL,
                ConjunctivaCommentOD TEXT,
                ConjunctivaOI CHECK(ConjunctivaOI IN ('Normal', 'Anormal')) NOT NULL,
                ConjunctivaCommentOI TEXT,
                
                CorneaOD CHECK(CorneaOD IN ('Normal', 'Anormal')) NOT NULL,
                CorneaCommentOD TEXT,
                CorneaOI CHECK(CorneaOI IN ('Normal', 'Anormal')) NOT NULL,
                CorneaCommentOI TEXT,
                
                IrisOD CHECK(IrisOD IN ('Normal', 'Anormal')) NOT NULL,
                IrisCommentOD TEXT,
                IrisOI CHECK(IrisOI IN ('Normal', 'Anormal')) NOT NULL,
                IrisCommentOI TEXT,
                
                PupilOD CHECK(PupilOD IN ('Normal', 'Anormal')) NOT NULL,
                PupilCommentOD TEXT,
                PupilOI CHECK(PupilOI IN ('Normal', 'Anormal')) NOT NULL,
                PupilCommentOI TEXT,
                
                LenteOD CHECK(LenteOD IN ('Normal', 'Anormal')) NOT NULL,
                LenteCommentOD TEXT,
                LenteOI CHECK(LenteOI IN ('Normal', 'Anormal')) NOT NULL,
                LenteCommentOI TEXT,
                
                CdOD TEXT NOT NULL,
                CdOI TEXT NOT NULL,

                NerveOD CHECK(NerveOD IN ('Normal', 'Anormal')) NOT NULL,
                NerveCommentOD TEXT, 
                NerveOI CHECK(NerveOI IN ('Normal', 'Anormal')) NOT NULL,
                NerveCommentOI TEXT, 
                
                MaculaOD CHECK(MaculaOD IN ('Normal', 'Anormal')) NOT NULL,
                MaculaCommentOD TEXT,
                MaculaOI CHECK(MaculaOI IN ('Normal', 'Anormal')) NOT NULL,
                MaculaCommentOI TEXT,
                
                VasculatureOD CHECK(VasculatureOD IN ('Normal', 'Anormal')) NOT NULL,
                VasculatureCommentOD TEXT,
                VasculatureOI CHECK(VasculatureOI IN ('Normal', 'Anormal')) NOT NULL,
                VasculatureCommentOI TEXT,
                
                PeripheryOD CHECK(PeripheryOD IN ('Normal', 'Anormal')) NOT NULL,
                PeripheryCommentOD TEXT, 
                PeripheryOI CHECK(PeripheryOI IN ('Normal', 'Anormal')) NOT NULL,
                PeripheryCommentOI TEXT,
                
                VitreousOD CHECK(VitreousOD IN ('Normal', 'Anormal')) NOT NULL,
                VitreousCommentOD TEXT,
                VitreousOI CHECK(VitreousOI IN ('Normal', 'Anormal')) NOT NULL,
                VitreousCommentOI TEXT
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Diagnosis(
                DiagnosisMyopia BIT, 
                DiagnosisHyperopia BIT, 
                DiagnosisAstigmatism BIT, 
                DiagnosisComment TEXT, 
                Treatment TEXT
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Addendum(
                Addendum TEXT,
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP, 
                RecordID INTEGER NOT NULL,
                DoctorID INTEGER NOT NULL,
                FOREIGN KEY (RecordID) REFERENCES Record(_rowid_),
                FOREIGN Key (DoctorID) REFERENCES Doctor(_rowid_)
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Record(
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                LastEditedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                ReasonForVisit TEXT NOT NULL,
                StudentID INTEGER NOT NULL,
                DoctorID INTEGER NOT NULL,
                VisionDistanceID INTEGER NOT NULL,
                DilatationID INTEGER NOT NULL,
                RefractiveStatusID INTEGER NOT NULL, 
                GlassesPrescriptionID INTEGER NOT NULL, 
                OcularAssessmentTableID INTEGER NOT NULL, 
                DiagnosisID INTEGER NOT NULL, 
                FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
                FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID),
                FOREIGN KEY (VisionDistanceID) REFERENCES VisionDistance(_rowid_),
                FOREIGN KEY (DilatationID) REFERENCES Dilatation(_rowid_),
                FOREIGN KEY (RefractiveStatusID) REFERENCES RefractiveStatus(_rowid_), 
                FOREIGN KEY (GlassesPrescriptionID) REFERENCES GlassesPrescription(_rowid_), 
                FOREIGN KEY (OcularAssessmentTableID) REFERENCES OcularAssessmentTable(_rowid_), 
                FOREIGN KEY (DiagnosisID) REFERENCES Diagnosis(_rowid_)
                )''')

def insert_school(cur, name):
    cur.execute('''INSERT INTO School(Name) VALUES (?)''', (name,))
    cur.connection.commit()
    return cur.lastrowid

def insert_student(cur, student_id, firstname, lastname, birthday, phone_number, school_id):
    cur.execute(f'''INSERT INTO Student(StudentID, FirstName, LastName, DateOfBirth, PhoneNumber, SchoolID) 
                    VALUES(?, ?, ?, ?, ?, ?)''', (student_id, firstname, lastname, birthday, phone_number, school_id))
    cur.connection.commit()

def insert_doctor(cur, doctor_id, firstname, lastname):
    cur.execute('''INSERT INTO doctor(DoctorID, FirstName, LastName) VALUES(?, ?, ?)''', (doctor_id, firstname, lastname))
    cur.connection.commit()

def insert_vision_distance(cur, vision_distance_method, vision_distance_od, vision_distance_oi):
    cur.execute('''INSERT INTO VisionDistance(VisionDistanceMethod, VisionDistanceOD, VisionDistanceOI) VALUES(?, ?, ?)''', 
                (vision_distance_method, vision_distance_od, vision_distance_oi))
    cur.connection.commit()
    return cur.lastrowid

def insert_intraocular_pressure(cur, intraocular_pressure_method, intraocular_pressure_od, intraocular_pressure_od_timestamp, intraocular_pressure_oi, intraocular_pressure_oi_timestamp, record_id):
    cur.execute('''INSERT INTO IntraocularPressure(IntraocularPressureMethod, IntraocularPressureOD, IntraocularPressureODTimestamp, IntraocularPressureOI, IntraocularPressureOITimestamp, RecordID) VALUES(?, ?, ?, ?, ?, ?)''',
                (intraocular_pressure_method, intraocular_pressure_od, intraocular_pressure_od_timestamp, intraocular_pressure_oi, intraocular_pressure_oi_timestamp, record_id))
    cur.connection.commit()
    return cur.lastrowid

def insert_dilatation(cur, dilatation, dilatation_timestamp):
    cur.execute('''INSERT INTO Dilatation(Dilatation, DilatationTimestamp) VALUES(?, ?)''', (dilatation, dilatation_timestamp))
    cur.connection.commit()
    return cur.lastrowid

def insert_refractive_status(cur, refractive_status_method, refractive_status_sphere_od, refractive_status_sphere_oi, refractive_status_cylinder_od, 
                             refractive_status_cylinder_oi, refractive_status_axis_od, refractive_status_axis_oi):
    cur.execute('''INSERT INTO RefractiveStatus(RefractiveStatusMethod, RefractiveStatusSphereOD, RefractiveStatusSphereOI, 
                RefractiveStatusCylinderOD, RefractiveStatusCylinderOI, RefractiveStatusAxisOD, RefractiveStatusAxisOI) VALUES(?, ?, ?, ?, ?, ?, ?)''',
                (refractive_status_method, refractive_status_sphere_od, refractive_status_sphere_oi, refractive_status_cylinder_od, refractive_status_cylinder_oi, refractive_status_axis_od, refractive_status_axis_oi))
    cur.connection.commit()
    return cur.lastrowid

def insert_glasses_prescription(cur, glasses_prescription_sphere_od, glasses_prescription_sphere_oi, glasses_prescription_cylinder_od, glasses_prescription_cylinder_oi, 
                                glasses_prescription_axis_od, glasses_prescription_axis_oi, glasses_prescription_dva_od, glasses_prescription_dva_oi, glasses_prescription_pd):
    cur.execute('''INSERT INTO GlassesPrescription(GlassesPrescriptionSphereOD, GlassesPrescriptionSphereOI, GlassesPrescriptionCylinderOD, GlassesPrescriptionCylinderOI, 
                GlassesPrescriptionAxisOD, GlassesPrescriptionAxisOI, GlassesPrescriptionDvaOD, GlassesPrescriptionDvaOI, GlassesPrescriptionPD) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (glasses_prescription_sphere_od, glasses_prescription_sphere_oi, glasses_prescription_cylinder_od, glasses_prescription_cylinder_oi, glasses_prescription_axis_od, 
                 glasses_prescription_axis_oi, glasses_prescription_dva_od, glasses_prescription_dva_oi, glasses_prescription_pd))
    cur.connection.commit()
    return cur.lastrowid

def insert_ocular_assessment_table(cur, eyelid_od, eyelid_comment_od, eyelid_oi, eyelid_comment_oi, conjunctiva_od, conjunctiva_comment_od, conjunctiva_oi, conjunctiva_comment_oi, cornea_od, cornea_comment_od, cornea_oi, cornea_comment_oi, 
                                   iris_od, iris_comment_od, iris_oi, iris_comment_oi, pupil_od, pupil_comment_od, pupil_oi, pupil_comment_oi, lente_od, lente_comment_od, lente_oi, lente_comment_oi, cd_od, cd_oi, nerve_od, nerve_comment_od, 
                                   nerve_oi, nerve_comment_oi, macula_od, macula_comment_od, macula_oi, macula_comment_oi, vasculature_od, vasculature_comment_od, vasculature_oi, vasculature_comment_oi, periphery_od, periphery_comment_od, 
                                   periphery_oi, periphery_comment_oi, vitreous_od, vitreous_comment_od, vitreous_oi, vitreous_comment_oi):
    cur.execute('''INSERT INTO OcularAssessmentTable(EyelidOD, EyelidCommentOD, EyelidOI, EyelidCommentOI, ConjunctivaOD, ConjunctivaCommentOD, ConjunctivaOI, ConjunctivaCommentOI, CorneaOD, CorneaCommentOD, CorneaOI, CorneaCommentOI,
                IrisOD, IrisCommentOD, IrisOI, IrisCommentOI, PupilOD, PupilCommentOD, PupilOI, PupilCommentOI, LenteOD, LenteCommentOD, LenteOI, LenteCommentOI, CdOD, CdOI, NerveOD, NerveCommentOD, NerveOI, NerveCommentOI, MaculaOD,
                MaculaCommentOD, MaculaOI, MaculaCommentOI, VasculatureOD, VasculatureCommentOD, VasculatureOI, VasculatureCommentOI, PeripheryOD, PeripheryCommentOD, PeripheryOI, PeripheryCommentOI, VitreousOD, VitreousCommentOD, VitreousOI, VitreousCommentOI) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                (eyelid_od, eyelid_comment_od, eyelid_oi, eyelid_comment_oi, conjunctiva_od, conjunctiva_comment_od, conjunctiva_oi, conjunctiva_comment_oi, cornea_od, cornea_comment_od, cornea_oi, cornea_comment_oi, iris_od, iris_comment_od,
                 iris_oi, iris_comment_oi, pupil_od, pupil_comment_od, pupil_oi, pupil_comment_oi, lente_od, lente_comment_od, lente_oi, lente_comment_oi, cd_od, cd_oi, nerve_od, nerve_comment_od, nerve_oi, nerve_comment_oi, macula_od,
                 macula_comment_od, macula_oi, macula_comment_oi, vasculature_od, vasculature_comment_od, vasculature_oi, vasculature_comment_oi, periphery_od, periphery_comment_od, periphery_oi, periphery_comment_oi, vitreous_od, vitreous_comment_od,
                 vitreous_oi, vitreous_comment_oi))
    cur.connection.commit()
    return cur.lastrowid

def insert_diagnosis(cur, diagnosis_myopia, diagnosis_hyperopia, diagnosis_astigmatism, diagnosis_comment, treatment):
    cur.execute('''INSERT INTO Diagnosis(DiagnosisMyopia, DiagnosisHyperopia, DiagnosisAstigmatism, DiagnosisComment, Treatment) VALUES(?, ?, ?, ?, ?)''', 
                (diagnosis_myopia, diagnosis_hyperopia, diagnosis_astigmatism, diagnosis_comment, treatment))
    cur.connection.commit()
    return cur.lastrowid

def insert_addendum(cur, created_at, addendum, record_id, doctor_id):
    cur.execute('''INSERT INTO Addendum(Addendum, CreatedAt, RecordID, DoctorID) VALUES(?, ?, ?, ?)''', (addendum, created_at, record_id, doctor_id))
    cur.connection.commit()
    return cur.lastrowid

def insert_record(cur, created_at, last_edited_at, reason_for_visit, student_id, doctor_id, vision_distance_id, 
                  dilatation_id, refractiveStatus_id, glassesPrescription_id, ocularAssessmentTable_id, diagnosis_id):
    cur.execute('''INSERT INTO Record(CreatedAt, LastEditedAt, ReasonForVisit, StudentID, DoctorID, VisionDistanceID, 
                DilatationID, RefractiveStatusID, GlassesPrescriptionID, OcularAssessmentTableID, DiagnosisID) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                (created_at, last_edited_at, reason_for_visit, student_id, doctor_id, vision_distance_id, dilatation_id, refractiveStatus_id, glassesPrescription_id, ocularAssessmentTable_id, diagnosis_id))
    cur.connection.commit()
    return cur.lastrowid

def fetch_row(cur, table, column, value): 
    return cur.execute(f'''SELECT _rowid_, * FROM {table} WHERE {column} = ?''', (value,)).fetchone()

def fetch_all_rows(cur, table, column, value, order_by=None): 
    if order_by: 
        cmd = f" ORDER BY {order_by}"
    else: 
        cmd = ""
    return cur.execute(f'''SELECT _rowid_, * FROM {table} WHERE {column} = ?{cmd}''', (value,)).fetchall()

def fetch_record(cur, firstname, lastname, dob): 
    id = utils.generate_id(firstname, lastname, dob)
    records = cur.execute('''SELECT _rowid_, * FROM Record WHERE StudentID = ? ORDER BY LastEditedAt DESC''', (id,)).fetchall()
    data = []
    for record in records: 
        id = record[0]

        student = fetch_row(cur, "Student", "StudentID", record[4])
        school = fetch_row(cur, "School", "_rowid_", student[6])
        doctor = fetch_row(cur, "Doctor", "DoctorID", record[5])
        vd = fetch_row(cur, "VisionDistance", "_rowid_", record[6])
        dilatation = fetch_row(cur, "Dilatation", "_rowid_", record[7])
        rs = fetch_row(cur, "RefractiveStatus", "_rowid_", record[8])
        gp = fetch_row(cur, "GlassesPrescription", "_rowid_", record[9])
        oa_table = fetch_row(cur, "OcularAssessmentTable", "_rowid_", record[10])
        diagnosis = fetch_row(cur, "Diagnosis", "_rowid_", record[11])

        ip = fetch_all_rows(cur, "IntraocularPressure", "RecordID", id)
        addendum = fetch_all_rows(cur, "Addendum", "RecordID", id, "CreatedAt")

        record_data = {
            "RecordID": id,
            "CreatedAt": record[1], 
            "LastEditedAt": record[2], 
            "ReasonForVisit": record[3], 
            "Student": student, 
            "School": school,
            "Doctor": doctor, 
            "VisionDistance": vd, 
            "Dilatation": dilatation, 
            "RefractiveStatus": rs, 
            "GlassesPrescription": gp, 
            "OcularAssessmentTable": oa_table, 
            "Diagnosis": diagnosis, 
            "IntraocularPressure": ip, 
            "Addendum": addendum}
        data.append(record_data)
    return data

def update_record_last_edit_time(cur, id, time): 
    cur.execute('''UPDATE Record SET LastEditedAt = ? WHERE _rowid_ = ?''', (time, id))