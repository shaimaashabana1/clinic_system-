import streamlit as st
import pandas as pd
from PatientManager import PatientManager
from DoctorManager import DoctorManager
from AppointmentManager import AppointmentManager
from MedicalRecordManager import MedicalRecordManager

# Initialize Managers
pm = PatientManager()
dm = DoctorManager()
am = AppointmentManager()
rm = MedicalRecordManager()

st.set_page_config(page_title="Clinic Master System", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 Clinic Management System")

menu = st.sidebar.selectbox("Main Navigation", 
    ["Patients", "Doctors", "Appointments", "Medical Records", "Overview"])

# Helper function to display dataframes
def show_table(data, cols):
    if data:
        st.dataframe(pd.DataFrame(data, columns=cols), use_container_width=True)
    else:
        st.info("No records found.")

# ==================== PATIENTS SECTION ====================
if menu == "Patients":
    st.header("👤 Patient Management")
    t1, t2, t3, t4 = st.tabs(["Add New", "Search & Update", "Delete", "All Patients"])
    
    with t1:
        with st.form("add_p"):
            name = st.text_input("Full Name")
            age = st.number_input("Age", 1, 120)
            phone = st.text_input("Phone Number")
            if st.form_submit_button("Save Patient"):
                new_id = pm.add_patient(name, str(age), phone)
                st.success(f"Patient Added Successfully! ID: {new_id}")

    with t2:
        sid = st.text_input("Search by Patient ID")
        p_data = pm.get_patient(sid)
        if p_data:
            st.table(pd.DataFrame([p_data], columns=["ID", "Name", "Age", "Phone"]))
            st.subheader("Update Information")
            new_n = st.text_input("New Name (leave blank to keep current)")
            new_a = st.text_input("New Age")
            new_p = st.text_input("New Phone")
            if st.button("Update Patient"):
                pm.update_patient(sid, new_n or None, new_a or None, new_p or None)
                st.success("Record Updated!")
        elif sid: st.error("Patient not found.")

    with t3:
        did = st.text_input("Enter Patient ID to Delete")
        if st.button("Permanently Delete", type="primary"):
            if pm.delete_patient(did):
                am.delete_by_patient(did) # Clean up appointments
                st.warning("Patient and all related appointments deleted.")
            else: st.error("Invalid ID.")

    with t4:
        show_table(pm.list_patients(), ["ID", "Name", "Age", "Phone"])

# ==================== DOCTORS SECTION ====================
elif menu == "Doctors":
    st.header("🩺 Doctor Management")
    t1, t2, t3 = st.tabs(["Manage Doctors", "Search by Specialty", "Doctor List"])
    
    with t1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Add Doctor")
            dn = st.text_input("Doctor Name")
            ds = st.text_input("Specialty")
            if st.button("Add"):
                st.success(f"Doctor Added! ID: {dm.add_doctor(dn, ds)}")
        with col2:
            st.subheader("Update Doctor")
            udid = st.text_input("Doctor ID to update")
            udn = st.text_input("New Name")
            uds = st.text_input("New Specialty")
            if st.button("Update"):
                if dm.update_doctor(udid, udn or None, uds or None): st.success("Updated!")

    with t2:
        spec = st.text_input("Enter Specialty (e.g., Surgery, Dental)")
        if st.button("Search Specialty"):
            show_table(dm.search_by_specialty(spec), ["ID", "Name", "Specialty"])

    with t3:
        show_table(dm.list_doctors(), ["ID", "Name", "Specialty"])
        del_dr = st.text_input("Enter Doctor ID to Delete")
        if st.button("Delete Doctor", key="del_dr_btn"):
            if dm.delete_doctor(del_dr):
                am.delete_by_doctor(del_dr)
                st.success("Doctor deleted.")

# ==================== APPOINTMENTS SECTION ====================
elif menu == "Appointments":
    st.header("📅 Appointment Scheduling")
    t1, t2, t3 = st.tabs(["Book Appointment", "Daily Agenda", "Cancel Appointment"])
    
    with t1:
        p_id = st.text_input("Patient ID")
        d_id = st.text_input("Doctor ID")
        d_t = st.text_input("Time (YYYY-MM-DD HH:MM)")
        if st.button("Confirm Booking"):
            res = am.add_appointment(p_id, d_id, d_t)
            if res: st.success(f"Appointment Booked! ID: {res}")
            else: st.error("Date format error! Use: YYYY-MM-DD HH:MM")

    with t2:
        st.subheader("Today's General Agenda")
        show_table(am.daily_agenda(), ["AID", "PID", "DID", "Time"])
        st.divider()
        st.subheader("Doctor Specific Schedule")
        dr_search = st.text_input("Enter Doctor ID for Today's Schedule")
        if st.button("Show Schedule"):
            show_table(am.doctor_schedule_today(dr_search), ["AID", "PID", "DID", "Time"])

    with t3:
        can_id = st.text_input("Appointment ID to Cancel")
        if st.button("Cancel Appointment"):
            am.cancel_appointment(can_id)
            rm.delete_by_appointment(can_id)
            st.success("Appointment canceled and medical record removed.")

# ==================== MEDICAL RECORDS SECTION ====================
elif menu == "Medical Records":
    st.header("📄 Medical Records")
    t1, t2 = st.tabs(["Save Diagnosis", "View/Delete Records"])
    
    with t1:
        a_id = st.text_input("Appointment ID")
        diag = st.text_area("Diagnosis Details")
        med = st.text_input("Prescribed Medication")
        if st.button("Save Record"):
            rm.add_or_update(a_id, diag, med)
            st.success("Medical record saved.")

    with t2:
        v_aid = st.text_input("Enter Appointment ID to view Record")
        if st.button("View"):
            rec = rm.get_by_appointment(v_aid)
            if rec:
                st.info(f"**Diagnosis:** {rec[2]}\n\n**Medication:** {rec[3]}")
            else: st.error("No record found for this ID.")
        
        if st.button("Delete Medical Record"):
            rm.delete_by_appointment(v_aid)
            st.success("Record deleted.")

# ==================== OVERVIEW SECTION ====================
elif menu == "Overview":
    st.header("📊 Dashboard Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Patients", len(pm.list_patients()))
    c2.metric("Total Doctors", len(dm.list_doctors()))
    c3.metric("Appointments Today", len(am.daily_agenda()))
    
    st.subheader("All Registered Appointments")
    show_table(am.list_appointments(), ["AID", "PID", "DID", "Time"])