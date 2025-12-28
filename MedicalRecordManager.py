import csv

class MedicalRecordManager:
    def __init__(self, file="medical_records.csv"):
        self.file = file
        self._init_file()

    def _init_file(self):
        try:
            open(self.file, "r").close()
        except FileNotFoundError:
            with open(self.file, "w", newline="") as f:
                csv.writer(f).writerow(
                    ["appointment_id", "diagnosis", "treatment"]
                )

    # FR: Record / Update Diagnosis
    def record_diagnosis(self, appointment_id, diagnosis, treatment):
        with open(self.file, "r") as f:
            rows = list(csv.reader(f))

        for row in rows[1:]:
            if row[0] == str(appointment_id):
                row[1] = diagnosis
                row[2] = treatment
                break
        else:
            rows.append([appointment_id, diagnosis, treatment])

        with open(self.file, "w", newline="") as f:
            csv.writer(f).writerows(rows)

    # FR: View Diagnosis
    def view_diagnosis(self, appointment_id):
        with open(self.file, "r") as f:
            return [
                r for r in list(csv.reader(f))[1:]
                if r[0] == str(appointment_id)
            ]
