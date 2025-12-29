import csv, os

class PatientManager:
    def __init__(self, file="patients.csv"):
        self.file = file
        if not os.path.exists(self.file):
            with open(self.file, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["patient_id", "name", "age", "phone"])

    def _next_id(self):
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                rows = list(csv.reader(f))
                return int(rows[-1][0]) + 1 if len(rows) > 1 else 1
        except: return 1

    def add_patient(self, name, age, phone):
        pid = self._next_id()
        with open(self.file, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([pid, name, age, phone])
        return pid

    def list_patients(self):
        if not os.path.exists(self.file): return []
        with open(self.file, "r", encoding="utf-8") as f:
            return list(csv.reader(f))[1:]

    def get_patient(self, pid):
        for p in self.list_patients():
            if str(p[0]).strip() == str(pid).strip(): return p
        return None

    def update_patient(self, pid, name=None, age=None, phone=None):
        rows = self.list_patients()
        updated = False
        for p in rows:
            if str(p[0]).strip() == str(pid).strip():
                if name: p[1] = name
                if age: p[2] = age
                if phone: p[3] = phone
                updated = True
                break
        if updated: self._save(rows)
        return updated

    def delete_patient(self, pid):
        rows = self.list_patients()
        new = [p for p in rows if str(p[0]).strip() != str(pid).strip()]
        if len(rows) == len(new): return False
        self._save(new)
        return True

    def _save(self, rows):
        with open(self.file, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["patient_id", "name", "age", "phone"])
            w.writerows(rows)