import csv

class DoctorManager:
    def __init__(self, doctor_file="doctors.csv"):
        self.doctor_file = doctor_file
        self.create_file_if_not_exist()

    def create_file_if_not_exist(self):
        try:
            with open(self.doctor_file, "r"):
                pass
        except FileNotFoundError:
            with open(self.doctor_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["doctor_id", "name", "specialty", "phone"])

    def add_doctor(self, doctor_id, name, specialty, phone):
        with open(self.doctor_file, "a", newline="") as f:
            csv.writer(f).writer.writerow([doctor_id, name, specialty, phone])
        print("Doctor added.")

    def update_doctor(self, doctor_id, name=None, specialty=None, phone=None):
        try:
            with open(self.doctor_file, "r") as f:
                rows = list(csv.reader(f))
        except:
            print("File missing.")
            return

        updated = False
        for row in rows[1:]:
            if row[0] == str(doctor_id):
                if name: row[1] = name
                if specialty: row[2] = specialty
                if phone: row[3] = phone
                updated = True
                break

        if updated:
            with open(self.doctor_file, "w", newline="") as f:
                csv.writer(f).writerows(rows)
            print("Doctor updated.")
        else:
            print("Doctor not found.")

    def delete_doctor(self, doctor_id):
        try:
            with open(self.doctor_file, "r") as f:
                rows = list(csv.reader(f))
        except:
            print("File missing.")
            return

        new_rows = [rows[0]]
        deleted = False

        for row in rows[1:]:
            if row[0] != str(doctor_id):
                new_rows.append(row)
            else:
                deleted = True

        if deleted:
            with open(self.doctor_file, "w", newline="") as f:
                csv.writer(f).writerows(new_rows)
            print("Doctor deleted.")
        else:
            print("Doctor not found.")
