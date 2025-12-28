import csv
from datetime import datetime

class AppointmentManager:
    def __init__(self, file="appointments.csv"):
        self.file = file
        self._init_file()

    def _init_file(self):
        try:
            open(self.file, "r").close()
        except FileNotFoundError:
            with open(self.file, "w", newline="") as f:
                csv.writer(f).writerow(
                    ["appointment_id", "patient_id", "doctor_id", "date", "time"]
                )

    def _generate_id(self):
        with open(self.file, "r") as f:
            return len(list(csv.reader(f)))

    # FR: Date Validation
    def validate_date(self, date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except:
            return False

    # FR: Book Appointment
    def book_appointment(self, patient_id, doctor_id, date, time):
        if not self.validate_date(date):
            return None

        aid = self._generate_id()
        with open(self.file, "a", newline="") as f:
            csv.writer(f).writerow([aid, patient_id, doctor_id, date, time])
        return aid

    # FR: Update Appointment
    def update_appointment(self, appointment_id, date=None, time=None):
        with open(self.file, "r") as f:
            rows = list(csv.reader(f))

        for row in rows[1:]:
            if row[0] == str(appointment_id):
                if date and self.validate_date(date):
                    row[3] = date
                if time:
                    row[4] = time

        with open(self.file, "w", newline="") as f:
            csv.writer(f).writerows(rows)

    # FR: Cancel Appointment
    def cancel_appointment(self, appointment_id):
        with open(self.file, "r") as f:
            rows = list(csv.reader(f))

        rows = [rows[0]] + [r for r in rows[1:] if r[0] != str(appointment_id)]

        with open(self.file, "w", newline="") as f:
            csv.writer(f).writerows(rows)

    # FR: Daily Agenda
    def daily_agenda(self, date):
        with open(self.file, "r") as f:
            return [r for r in list(csv.reader(f))[1:] if r[3] == date]

    # FR: Doctor Schedule
    def doctor_schedule(self, doctor_id, date):
        with open(self.file, "r") as f:
            return [
                r for r in list(csv.reader(f))[1:]
                if r[2] == str(doctor_id) and r[3] == date
            ]
