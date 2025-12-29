import csv, os

class MedicalRecordManager:
    def __init__(self, file="records.csv"):
        self.file = file
        if not os.path.exists(self.file):
            with open(self.file, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["record_id", "appointment_id", "diagnosis", "medication"])

    def _next_id(self):
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                rows = list(csv.reader(f))
                return int(rows[-1][0]) + 1 if len(rows) > 1 else 1
        except: return 1

    def add_or_update(self, aid, diag, med):
        rows = self.list_records()
        updated = False
        for r in rows:
            if str(r[1]) == str(aid):
                r[2], r[3] = diag, med
                updated = True
                break
        if not updated:
            rows.append([self._next_id(), aid, diag, med])
        self._save(rows)

    def list_records(self):
        if not os.path.exists(self.file): return []
        with open(self.file, "r", encoding="utf-8") as f:
            return list(csv.reader(f))[1:]

    def get_by_appointment(self, aid):
        for r in self.list_records():
            if str(r[1]) == str(aid): return r
        return None

    def delete_by_appointment(self, aid):
        rows = self.list_records()
        new = [r for r in rows if str(r[1]) != str(aid)]
        self._save(new)

    def _save(self, rows):
        with open(self.file, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["record_id", "appointment_id", "diagnosis", "medication"])
            w.writerows(rows)