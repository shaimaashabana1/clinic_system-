import streamlit as st
from PatientManager import PatientManager
from DoctorManager import DoctorManager
from AppointmentManager import AppointmentManager
from MedicalRecordManager import MedicalRecordManager

# Initialize Managers
patients = PatientManager()
doctors = DoctorManager()
appointments = AppointmentManager()
records = MedicalRecordManager()

st.set_page_config(page_title="Clinic Management System", layout="centered")
st.title("🏥 Clinic Management System")

section = st.sidebar.selectbox(
    "Choose Section",
    [
        "Patients",
        "Doctors",
        "Appointments",
        "Medical Diagnosis",
        "Daily Agenda",
        "Doctor Schedule"
    ]
)

# ==========================================================
# PATIENTS
# ==========================================================
if section == "Patients":
    action = st.selectbox(
        "Action",
        ["Add Patient", "Search Patient", "Update Patient", "Delete Patient", "List Patients"]
    )

    if action == "Add Patient":
        name = st.text_input("Name")
        age = st.number_input("Age", 1, 120)
        phone = st.text_input("Phone")

        if st.button("Add"):
            pid = patients.add_patient(name, age, phone)
            st.success(f"Patient added with ID: {pid}")

    elif action == "Search Patient":
        pid = st.text_input("Patient ID")
        if st.button("Search"):
            result = patients.search_patient(pid)
            if result:
                st.write(result)
            else:
                st.error("Patient not found")

    elif action == "Update Patient":
        pid = st.text_input("Patient ID")
        name = st.text_input("New Name")
        age = st.text_input("New Age")
        phone = st.text_input("New Phone")

        if st.button("Update"):
            patients.update_patient(
                pid,
                name if name else None,
                age if age else None,
                phone if phone else None
            )
            st.success("Patient updated")

    elif action == "Delete Patient":
        pid = st.text_input("Patient ID")
        if st.button("Delete"):
            patients.delete_patient(pid)
            st.success("Patient deleted (cascade applied)")

    elif action == "List Patients":
        st.table(patients.list_patients())

# ==========================================================
# DOCTORS
# ==========================================================
elif section == "Doctors":
    action = st.selectbox(
        "Action",
        ["Add Doctor", "Search Doctor", "Update Doctor", "Delete Doctor"]
    )

    if action == "Add Doctor":
        name = st.text_input("Doctor Name")
        specialty = st.text_input("Specialty")

        if st.button("Add"):
            did = doctors.add_doctor(name, specialty)
            st.success(f"Doctor added with ID: {did}")

    elif action == "Search Doctor":
        keyword = st.text_input("Search by Specialty")
        if st.button("Search"):
            result = doctors.search_doctor(keyword)
            st.table(result)

    elif action == "Update Doctor":
        did = st.text_input("Doctor ID")
        name = st.text_input("New Name")
        specialty = st.text_input("New Specialty")

        if st.button("Update"):
            doctors.update_doctor(
                did,
                name if name else None,
                specialty if specialty else None
            )
            st.success("Doctor updated")

    elif action == "Delete Doctor":
        did = st.text_input("Doctor ID")
        if st.button("Delete"):
            doctors.delete_doctor(did)
            st.success("Doctor deleted & appointments cancelled")

# ==========================================================
# APPOINTMENTS
# ==========================================================
elif section == "Appointments":
    action = st.selectbox(
        "Action",
        [
            "Book Appointment",
            "Update Appointment",
            "Cancel Appointment"
        ]
    )

    if action == "Book Appointment":
        pid = st.text_input("Patient ID")
        did = st.text_input("Doctor ID")
        date = st.text_input("Date (YYYY-MM-DD)")
        time = st.text_input("Time (HH:MM)")

        if st.button("Book"):
            aid = appointments.book_appointment(pid, did, date, time)
            if aid is None:
                st.error("Invalid date format")
            else:
                st.success(f"Appointment booked with ID: {aid}")

    elif action == "Update Appointment":
        aid = st.text_input("Appointment ID")
        date = st.text_input("New Date")
        time = st.text_input("New Time")

        if st.button("Update"):
            appointments.update_appointment(
                aid,
                date if date else None,
                time if time else None
            )
            st.success("Appointment updated")

    elif action == "Cancel Appointment":
        aid = st.text_input("Appointment ID")
        if st.button("Cancel"):
            appointments.cancel_appointment(aid)
            st.success("Appointment cancelled")

# ==========================================================
# MEDICAL DIAGNOSIS
# ==========================================================
elif section == "Medical Diagnosis":
    action = st.selectbox(
        "Action",
        ["Record Diagnosis", "View Diagnosis"]
    )

    if action == "Record Diagnosis":
        aid = st.text_input("Appointment ID")
        diagnosis = st.text_area("Diagnosis")
        treatment = st.text_area("Treatment")

        if st.button("Save"):
            records.record_diagnosis(aid, diagnosis, treatment)
            st.success("Diagnosis saved")

    elif action == "View Diagnosis":
        aid = st.text_input("Appointment ID")
        if st.button("View"):
            result = records.view_diagnosis(aid)
            st.write(result)

# ==========================================================
# DAILY AGENDA
# ==========================================================
elif section == "Daily Agenda":
    date = st.text_input("Date (YYYY-MM-DD)")
    if st.button("View"):
        result = appointments.daily_agenda(date)
        st.table(result)

# ==========================================================
# DOCTOR SCHEDULE
# ==========================================================
elif section == "Doctor Schedule":
    did = st.text_input("Doctor ID")
    date = st.text_input("Date (YYYY-MM-DD)")
    if st.button("View"):
        result = appointments.doctor_schedule(did, date)
        st.table(result)
