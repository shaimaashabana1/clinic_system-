import csv

class PatientManager:
    def __init__(self, file="patients.csv"):
        self.file = file
        self._init_file()

    def _init_file(self):
        try:
            open(self.file, "r").close()
        except FileNotFoundError:
            with open(self.file, "w", newline="") as f:
                csv.writer(f).writerow(
                    ["patient_id", "name", "age", "phone"]
                )

    def _generate_id(self):
        with open(self.file, "r") as f:
            return len(list(csv.reader(f)))

    # FR: Add Patient
    def add_patient(self, name, age, phone):
        pid = self._generate_id()
        with open(self.file, "a", newline="") as f:
            csv.writer(f).writerow([pid, name, age, phone])
        return pid

    # FR: Search Patient
    def search_patient(self, patient_id):
        with open(self.file, "r") as f:
            for row in list(csv.reader(f))[1:]:
                if row[0] == str(patient_id):
                    return row
        return None

    # FR: Update Patient
    def update_patient(self, patient_id, name=None, age=None, phone=None):
        with open(self.file, "r") as f:
            rows = list(csv.reader(f))

        for row in rows[1:]:
            if row[0] == str(patient_id):
                if name: row[1] = name
                if age: row[2] = age
                if phone: row[3] = phone

        with open(self.file, "w", newline="") as f:
            csv.writer(f).writerows(rows)

    # FR: Delete Patient (Cascade)
    def delete_patient(self, patient_id):
        with open(self.file, "r") as f:
            rows = list(csv.reader(f))

        rows = [rows[0]] + [r for r in rows[1:] if r[0] != str(patient_id)]

        with open(self.file, "w", newline="") as f:
            csv.writer(f).writerows(rows)

    # FR: List Patients
    def list_patients(self):
        with open(self.file, "r") as f:
            return list(csv.reader(f))[1:]
