import csv

class PatientManager:
    def __init__(self, patient_file="patients.csv"):
        self.patient_file = patient_file
        self.create_file_if_not_exist()

    def create_file_if_not_exist(self):
        try:
            with open(self.patient_file, "r"):
                pass
        except FileNotFoundError:
            with open(self.patient_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["patient_id", "name", "age", "gender", "phone"])

    def add_patient(self, patient_id, name, age, gender, phone):
        with open(self.patient_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([patient_id, name, age, gender, phone])
        print("Patient added successfully.")

    def update_patient(self, patient_id, name=None, age=None, gender=None, phone=None):
        try:
            with open(self.patient_file, "r") as f:
                rows = list(csv.reader(f))
        except:
            print("File not found.")
            return
        
        updated = False
        for row in rows[1:]:
            if row[0] == str(patient_id):
                if name: row[1] = name
                if age: row[2] = age
                if gender: row[3] = gender
                if phone: row[4] = phone
                updated = True
                break
        
        if updated:
            with open(self.patient_file, "w", newline="") as f:
                csv.writer(f).writerows(rows)
            print("Patient updated.")
        else:
            print("Patient not found.")

    def delete_patient(self, patient_id):
        try:
            with open(self.patient_file, "r") as f:
                rows = list(csv.reader(f))
        except:
            print("File not found.")
            return
        
        new_rows = [rows[0]]
        deleted = False

        for row in rows[1:]:
            if row[0] != str(patient_id):
                new_rows.append(row)
            else:
                deleted = True
        
        if deleted:
            with open(self.patient_file, "w", newline="") as f:
                csv.writer(f).writerows(new_rows)
            print("Patient deleted.")
        else:
            print("Patient not found.")

    def search_patient(self, patient_id=None, name=None):
        try:
            with open(self.patient_file, "r") as f:
                rows = list(csv.reader(f))
        except:
            print("File not found.")
            return

        found = False
        for row in rows[1:]:
            if patient_id and row[0] == str(patient_id):
                print(row)
                found = True
            elif name and row[1] == name:
                print(row)
                found = True

        if not found:
            print("No matching patient.")
