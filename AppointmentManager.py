import csv

class AppointmentManager:
    def _init_(self, appointment_file="appointment.csv"):
        self.appointment_file = appointment_file

    # ----- Create appointment -----
    def create_appointment(self, appointment_id, patient_id, doctor_id, date, time):
        try:
            with open(self.appointment_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([appointment_id, patient_id, doctor_id, date, time])
            print(f"Appointment {appointment_id} created successfully.")
        except Exception as e:
            print("Error creating appointment:", e)

    # ----- Update appointment -----
    def update_appointment(self, appointment_id, new_date=None, new_time=None, new_patient_id=None, new_doctor_id=None):
        try:
            with open(self.appointment_file, "r", newline="") as f:
                rows = list(csv.reader(f))
        except FileNotFoundError:
            print("Error: appointment file not found!")
            return

        if len(rows) <= 1:
            print("No appointments to update.")
            return

        updated = False
        for row in rows[1:]:
            if row[0] == str(appointment_id):
                if new_date: row[3] = new_date
                if new_time: row[4] = new_time
                if new_patient_id: row[1] = str(new_patient_id)
                if new_doctor_id: row[2] = str(new_doctor_id)
                updated = True
                break

        if not updated:
            print(f"No appointment found with ID: {appointment_id}")
            return

        with open(self.appointment_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print(f"Appointment {appointment_id} updated successfully.")

    # ----- Delete appointment -----
    def delete_appointment(self, appointment_id=None, delete_all=False):
        try:
            with open(self.appointment_file, "r", newline="") as f:
                rows = list(csv.reader(f))
        except FileNotFoundError:
            print("Error: appointment file not found!")
            return

        if len(rows) <= 1:
            print("No appointments to delete.")
            return

        if delete_all:
            with open(self.appointment_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(rows[0])  # keep header
            print("All appointments deleted.")
            return

        deleted = False
        new_rows = [rows[0]]  # keep header
        for row in rows[1:]:
            if row[0] != str(appointment_id):
                new_rows.append(row)
            else:
                deleted = True

        if deleted:
            with open(self.appointment_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(new_rows)
            print(f"Appointment {appointment_id} deleted successfully.")
        else:
            print(f"No appointment found with ID: {appointment_id}")

    # ----- Search appointments -----
    def search_appointment(self, appointment_id=None, date=None, time=None):
        try:
            with open(self.appointment_file, "r", newline="") as f:
                rows = list(csv.reader(f))
        except FileNotFoundError:
            print("Error: appointment file not found!")
            return

        if len(rows) <= 1:
            print("No appointments found.")
            return

        found = False
        for row in rows[1:]:
            match = False
            if appointment_id and row[0] == str(appointment_id):
                match = True
            elif date and time and row[3] == date and row[4] == time:
                match = True
            elif date and not time and row[3] == date:
                match = True

            if match:
                print(f"Appointment ID: {row[0]}, Patient ID: {row[1]}, Doctor ID: {row[2]}, Date: {row[3]}, Time: {row[4]}")
                found = True

        if not found:
            print("No matching appointment found.")

    # ----- Display appointments for patient -----
    def show_patient_appointments(self, patient_id, doctor_data=None):
        """
        doctor_data: dictionary {doctor_id: (doctor_name, specialty)}
        if provided, will display doctor name and specialty
        """
        try:
            with open(self.appointment_file, "r", newline="") as f:
                rows = list(csv.reader(f))
        except FileNotFoundError:
            print("Error: appointment file not found!")
            return

        if len(rows) <= 1:
            print("No appointments found.")
            return

        print(f"\n--- Appointments for Patient ID: {patient_id} ---")
        index = 1
        for row in rows[1:]:
            if row[1] == str(patient_id):
                doctor_id = row[2]
                if doctor_data:
                    doctor_name, specialty = doctor_data.get(doctor_id, ("Unknown", "Unknown"))
                    print(f"{index}. Doctor: {doctor_name} ({specialty}) | Date: {row[3]} | Time: {row[4]}")
                else:
                    print(f"{index}. Doctor ID: {doctor_id} | Date: {row[3]} | Time: {row[4]}")
                index += 1
        print("-----------------------------\n")

    # ----- Display appointments for doctor -----
    def show_doctor_appointments(self, doctor_id):
        try:
            with open(self.appointment_file, "r", newline="") as f:
                rows = list(csv.reader(f))
        except FileNotFoundError:
            print("Error: appointment file not found!")
            return

        if len(rows) <= 1:
            print("No appointments found.")
            return

        print(f"\n--- Appointments for Doctor ID: {doctor_id} ---")
        index = 1
        for row in rows[1:]:
            if row[2] == str(doctor_id):
                print(f"{index}. Patient ID: {row[1]} | Date: {row[3]} | Time: {row[4]}")
                index += 1
        print("-----------------------------\n")
