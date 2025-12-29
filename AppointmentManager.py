import csv, os
from datetime import datetime, date

class AppointmentManager:
    def __init__(self, file="appointments.csv"):
        self.file = file
        if not os.path.exists(self.file):
            with open(self.file, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["appointment_id", "patient_id", "doctor_id", "datetime"])

    def _next_id(self):
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                rows = list(csv.reader(f))
                return int(rows[-1][0]) + 1 if len(rows) > 1 else 1
        except: return 1

    def validate_date(self, dt):
        try:
            datetime.strptime(dt, "%Y-%m-%d %H:%M")
            return True
        except: return False

    def add_appointment(self, pid, did, dt):
        if not self.validate_date(dt): return None
        aid = self._next_id()
        with open(self.file, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([aid, pid, did, dt])
        return aid

    def list_appointments(self):
        if not os.path.exists(self.file): return []
        with open(self.file, "r", encoding="utf-8") as f:
            return list(csv.reader(f))[1:]

    def cancel_appointment(self, aid):
        rows = self.list_appointments()
        new = [a for a in rows if a[0] != str(aid)]
        self._save(new)

    def daily_agenda(self):
        today = date.today().isoformat()
        return [a for a in self.list_appointments() if a[3].startswith(today)]

    def doctor_schedule_today(self, did):
        today = date.today().isoformat()
        return [a for a in self.list_appointments() if str(a[2]) == str(did) and a[3].startswith(today)]

    # --- الدوال اللي كانت ناقصة وعملت المشكلة ---
    def delete_by_patient(self, pid):
        rows = self.list_appointments()
        new = [a for a in rows if str(a[1]) != str(pid)]
        self._save(new)

    def delete_by_doctor(self, did):
        rows = self.list_appointments()
        new = [a for a in rows if str(a[2]) != str(did)]
        self._save(new)

    def _save(self, rows):
        with open(self.file, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["appointment_id", "patient_id", "doctor_id", "datetime"])
            w.writerows(rows)