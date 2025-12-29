import csv, os

class DoctorManager:
    def __init__(self, file="doctors.csv"):
        self.file = file
        if not os.path.exists(self.file):
            with open(self.file, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["doctor_id", "name", "specialty"])

    def _next_id(self):
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                rows = list(csv.reader(f))
                return int(rows[-1][0]) + 1 if len(rows) > 1 else 1
        except: return 1

    def add_doctor(self, name, specialty):
        did = self._next_id()
        with open(self.file, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([did, name, specialty])
        return did

    def list_doctors(self):
        if not os.path.exists(self.file): return []
        with open(self.file, "r", encoding="utf-8") as f:
            return list(csv.reader(f))[1:]

    def search_by_specialty(self, keyword):
        return [d for d in self.list_doctors() if keyword.lower() in d[2].lower()]

    def update_doctor(self, did, name=None, specialty=None):
        rows = self.list_doctors()
        updated = False
        for d in rows:
            if str(d[0]).strip() == str(did).strip():
                if name: d[1] = name
                if specialty: d[2] = specialty
                updated = True
                break
        if updated: self._save(rows)
        return updated

    def delete_doctor(self, did):
        rows = self.list_doctors()
        new = [d for d in rows if str(d[0]).strip() != str(did).strip()]
        if len(rows) == len(new): return False
        self._save(new)
        return True

    def _save(self, rows):
        with open(self.file, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["doctor_id", "name", "specialty"])
            w.writerows(rows)