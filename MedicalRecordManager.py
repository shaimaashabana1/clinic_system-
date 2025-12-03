import csv

class MedicalRecordManager:
    def __init__(self, record_file="medical_records.csv"):
        self.record_file = record_file
        self.create_file_if_not_exist()

    def create_file_if_not_exist(self):
        try:
            with open(self.record_file, "r"):
                pass
        except FileNotFoundError:
            with open(self.record_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["record_id", "patient_id", "doctor_id", "diagnosis", "treatment", "date"])

    def add_record(self, record_id, patient_id, doctor_id, diagnosis, treatment, date):
        with open(self.record_file, "a", newline="") as f:
            csv.writer(f).writerow([record_id, patient_id, doctor_id, diagnosis, treatment, date])
        print("Medical record added.")

    def search_by_patient(self, patient_id):
        try:
            with open(self.record_file, "r") as f:
                rows = list(csv.reader(f))
        except:
            print("File missing.")
            return
        
        print(f"\n--- Records for Patient {patient_id} ---")
        for row in rows[1:]:
            if row[1] == str(patient_id):
                print(row)

    def delete_record(self, record_id):
        try:
            with open(self.record_file, "r") as f:
                rows = list(csv.reader(f))
        except:
            print("Missing file.")
            return

        new_rows = [rows[0]]
        deleted = False

        for row in rows[1:]:
            if row[0] != str(record_id):
                new_rows.append(row)
            else:
                deleted = True

        if deleted:
            with open(self.record_file, "w", newline="") as f:
                csv.writer(f).writerows(new_rows)
            print("Record deleted.")
        else:
            print("Record not found.")
