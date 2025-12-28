import csv

class DoctorManager:
    def __init__(self, file="doctors.csv"):
        self.file = file
        self._init_file()

    def _init_file(self):
        try:
            open(self.file, "r").close()
        except FileNotFoundError:
            with open(self.file, "w", newline="") as f:
                csv.writer(f).writerow(
                    ["doctor_id", "name", "specialty"]
                )

    def _generate_id(self):
        with open(self.file, "r") as f:
            return len(list(csv.reader(f)))

    # FR: Add Doctor
    def add_doctor(self, name, specialty):
        did = self._generate_id()
        with open(self.file, "a", newline="") as f:
            csv.writer(f).writerow([did, name, specialty])
        return did

    # FR: Search Doctor (partial specialty)
    def search_doctor(self, keyword):
        with open(self.file, "r") as f:
            return [
                r for r in list(csv.reader(f))[1:]
                if keyword.lower() in r[2].lower()
            ]

    # FR: Update Doctor
    def update_doctor(self, doctor_id, name=None, specialty=None):
        with open(self.file, "r") as f:
            rows = list(csv.reader(f))

        for row in rows[1:]:
            if row[0] == str(doctor_id):
                if name: row[1] = name
                if specialty: row[2] = specialty

        with open(self.file, "w", newline="") as f:
            csv.writer(f).writerows(rows)

    # FR: Delete Doctor
    def delete_doctor(self, doctor_id):
        with open(self.file, "r") as f:
            rows = list(csv.reader(f))

        rows = [rows[0]] + [r for r in rows[1:] if r[0] != str(doctor_id)]

        with open(self.file, "w", newline="") as f:
            csv.writer(f).writerows(rows)
