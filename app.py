import streamlit as st
from PatientManager import PatientManager
from DoctorManager import DoctorManager
from AppointmentManager import AppointmentManager
from MedicalRecordManager import MedicalRecordManager

# --- Initialize managers ---
patients = PatientManager()
doctors = DoctorManager()
appointments = AppointmentManager()
records = MedicalRecordManager()

# --- UI ---
st.title("Clinic Management System")

section = st.sidebar.selectbox(
    "Choose Section",
    ["Patients", "Doctors", "Appointments", "Medical Records"]
)

# ================================================================
# --------------------- PATIENTS SECTION --------------------------
# ================================================================
if section == "Patients":
    st.header("Patient Manager")

    action = st.selectbox("Choose Action", ["Add Patient", "Search Patient", "Delete Patient", "Update Patient"])

    # Add
    if action == "Add Patient":
        pid = st.text_input("Patient ID")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female"])
        phone = st.text_input("Phone Number")

        if st.button("Add"):
            patients.add_patient(pid, name, age, gender, phone)
            st.success("Patient Added Successfully")

    # Search
    elif action == "Search Patient":
        pid = st.text_input("Patient ID")
        if st.button("Search"):
            result = patients.search_patient(pid)
            st.write(result if result else "Not Found")

    # Delete
    elif action == "Delete Patient":
        pid = st.text_input("Patient ID")
        if st.button("Delete"):
            patients.delete_patient(pid)
            st.success("Deleted (If ID existed).")

    # Update
    elif action == "Update Patient":
        pid = st.text_input("Patient ID")

        name = st.text_input("New Name (optional)")
        age = st.number_input("New Age (optional)", min_value=0, max_value=120)
        gender = st.selectbox("New Gender (optional)", ["", "Male", "Female"])
        phone = st.text_input("New Phone (optional)")

        if st.button("Update"):
            patients.update_patient(
                pid,
                name if name else None,
                age if age > 0 else None,
                gender if gender else None,
                phone if phone else None,
            )
            st.success("Updated (If ID existed).")

# ================================================================
# --------------------- DOCTORS SECTION --------------------------
# ================================================================
elif section == "Doctors":
    st.header("Doctor Manager")

    action = st.selectbox("Choose Action", ["Add Doctor", "Search Doctor"])

    if action == "Add Doctor":
        did = st.text_input("Doctor ID")
        name = st.text_input("Name")
        specialization = st.text_input("Specialization")

        if st.button("Add"):
            doctors.add_doctor(did, name, specialization)
            st.success("Doctor Added")

    elif action == "Search Doctor":
        did = st.text_input("Doctor ID")
        if st.button("Search"):
            st.write(doctors.search_doctor(did))

# ================================================================
# ------------------ APPOINTMENTS SECTION -------------------------
# ================================================================
elif section == "Appointments":
    st.header("Appointment Manager")

    action = st.selectbox("Choose Action", ["Create", "Delete", "Update", "Search"])

    if action == "Create":
        aid = st.text_input("Appointment ID")
        patient = st.text_input("Patient Name")
        doctor = st.text_input("Doctor Name")
        date = st.text_input("Date (YYYY-MM-DD)")
        time = st.text_input("Time (HH:MM)")

        if st.button("Create"):
            appointments.create_appointment(aid, patient, doctor, date, time)
            st.success("Appointment Created")

    elif action == "Delete":
        aid = st.text_input("Appointment ID")
        if st.button("Delete"):
            appointments.delete_appointment(aid)
            st.success("Deleted")

    elif action == "Update":
        aid = st.text_input("Appointment ID")
        patient = st.text_input("New Patient Name (optional)")
        doctor = st.text_input("New Doctor Name (optional)")
        date = st.text_input("New Date (optional)")
        time = st.text_input("New Time (optional)")

        if st.button("Update"):
            appointments.update_appointment(
                aid,
                patient if patient else None,
                doctor if doctor else None,
                date if date else None,
                time if time else None,
            )
            st.success("Updated")

    elif action == "Search":
        aid = st.text_input("Appointment ID")
        if st.button("Search"):
            st.write(appointments.search_appointment(aid))

# ================================================================
# ------------------ MEDICAL RECORDS SECTION ----------------------
# ================================================================
elif section == "Medical Records":
    st.header("Medical Records Manager")

    action = st.selectbox("Choose Action", ["Add Record", "Search Record"])

    if action == "Add Record":
        rid = st.text_input("Record ID")
        pid = st.text_input("Patient ID")
        diagnosis = st.text_area("Diagnosis")
        treatment = st.text_area("Treatment")

        if st.button("Add"):
            records.add_record(rid, pid, diagnosis, treatment)
            st.success("Record Added")

    elif action == "Search Record":
        rid = st.text_input("Record ID")
        if st.button("Search"):
            st.write(records.search_record(rid))
