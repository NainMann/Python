import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
import os
import pickle
from sklearn.ensemble import RandomForestClassifier

FILE_NAME = "patients.csv"
MODEL_FILE = "ai_model.pkl"
DATASET_FILE = "C:/Users/ddhru/Desktop/Codes (VS CODE)/hospital_dataset.csv"
    
# ------------------ AI MODEL ------------------

def train_model():
    df = pd.read_csv(DATASET_FILE)

    X = df[['Age', 'BloodPressure', 'Glucose']]
    y = df['Outcome']

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)

def load_model():
    if not os.path.exists(MODEL_FILE):
        train_model()

    with open(MODEL_FILE, "rb") as f:
        return pickle.load(f)

ai_model = load_model()

# ------------------ Utility Functions ------------------

def parse_bp(bp_input):
    try:
        sys, dia = bp_input.split('/')
        return int(sys), int(dia)
    except:
        raise ValueError("Use BP format like 120/80")

def format_bp(sys, dia):
    return f"{int(sys)}/{int(dia)}"

def convert_bp_for_ai(sys, dia):
    return (sys + dia) / 2

def analyze_weekly_health(bp_list, sugar_list):
    avg_sys = np.mean([bp[0] for bp in bp_list])
    avg_dia = np.mean([bp[1] for bp in bp_list])
    avg_sugar = np.mean(sugar_list)
    return avg_sys, avg_dia, avg_sugar

def bp_category(sys, dia):
    if sys >= 140 or dia >= 90:
        return "High BP (Hypertension)"
    elif sys < 90 or dia < 60:
        return "Low BP"
    else:
        return "Normal BP"

def calculate_risk(age, sys, dia, sugar):
    if age <= 18:
        sugar_limit = 140
        bp_limit = (110, 70)
    elif age <= 40:
        sugar_limit = 140
        bp_limit = (120, 80)
    elif age <= 60:
        sugar_limit = 150
        bp_limit = (130, 85)
    else:
        sugar_limit = 160
        bp_limit = (140, 90)

    risk = "Normal"

    if sugar > sugar_limit:
        if age < 25:
            risk = "Pre-Diabetic"
        else:
            risk = "Diabetic"

    if sys > bp_limit[0] or dia > bp_limit[1]:
        if risk == "Normal":
            risk = "Hypertension"
        else:
            risk += " + Hypertension"

    return risk

def get_suggestion(risk):
    if "Diabetic" in risk:
        return "Reduce sugar, exercise, consult doctor"
    elif "Hypertension" in risk:
        return "Reduce salt, manage stress"
    elif "Pre-Diabetic" in risk:
        return "Control diet, avoid junk food"
    else:
        return "Healthy lifestyle"

# ------------------ AI Prediction ------------------

def predict_ai_risk(age, sys, dia, sugar):
    bp_avg = convert_bp_for_ai(sys, dia)
    data = [[age, bp_avg, sugar]]
    result = ai_model.predict(data)
    return "High Risk" if result[0] == 1 else "Low Risk"

# ------------------ Main Class ------------------

class HospitalSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")

        tk.Label(root, text="Name").grid(row=0, column=0)
        tk.Label(root, text="Age").grid(row=1, column=0)

        self.name = tk.Entry(root)
        self.age = tk.Entry(root)

        self.name.grid(row=0, column=1)
        self.age.grid(row=1, column=1)

        self.bp_entries = []
        self.sugar_entries = []

        for i in range(7):
            tk.Label(root, text=f"Day {i+1} BP (120/80)").grid(row=2+i, column=0)
            tk.Label(root, text=f"Day {i+1} Sugar").grid(row=2+i, column=2)

            bp_entry = tk.Entry(root)
            sugar_entry = tk.Entry(root)

            bp_entry.grid(row=2+i, column=1)
            sugar_entry.grid(row=2+i, column=3)

            self.bp_entries.append(bp_entry)
            self.sugar_entries.append(sugar_entry)

        tk.Button(root, text="Add Patient", command=self.add_patient).grid(row=10, column=0)
        tk.Button(root, text="Delete Patient", command=self.delete_patient).grid(row=10, column=1)
        tk.Button(root, text="View Patients", command=self.view_patients).grid(row=10, column=2)
        tk.Button(root, text="Generate Report", command=self.generate_report).grid(row=10, column=3)

    # ------------------ Add Patient ------------------

    def add_patient(self):
        try:
            name = self.name.get()
            age = int(self.age.get())

            bp_list = []
            sugar_list = []

            for i in range(7):
                bp = parse_bp(self.bp_entries[i].get())
                sugar = int(self.sugar_entries[i].get())

                bp_list.append(bp)
                sugar_list.append(sugar)

            avg_sys, avg_dia, avg_sugar = analyze_weekly_health(bp_list, sugar_list)

            # RULE + AI
            rule_risk = calculate_risk(age, avg_sys, avg_dia, avg_sugar)
            ai_risk = predict_ai_risk(age, avg_sys, avg_dia, avg_sugar)

            risk = f"{rule_risk} (AI: {ai_risk})"

            suggestion = get_suggestion(rule_risk)

            if ai_risk == "High Risk":
                suggestion += "\n⚠️ AI Alert: Immediate attention recommended"

            bp_status = bp_category(avg_sys, avg_dia)

            data = {
                "Name": name,
                "Age": age,
                "Avg_BP": format_bp(avg_sys, avg_dia),
                "Avg_Sugar": avg_sugar,
                "Risk": risk,
                "Suggestion": suggestion
            }

            df_new = pd.DataFrame([data])

            if os.path.exists(FILE_NAME):
                df = pd.read_csv(FILE_NAME)
                df = pd.concat([df, df_new], ignore_index=True)
            else:
                df = df_new

            df.to_csv(FILE_NAME, index=False)

            result_text = f"""
Patient Added Successfully!

Average BP: {format_bp(avg_sys, avg_dia)} ({bp_status})
Average Sugar: {avg_sugar:.2f}

Health Risk:
{risk}

Suggestion:
{suggestion}
"""
            messagebox.showinfo("Patient Report", result_text)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------ Delete ------------------

    def delete_patient(self):
        name = self.name.get()

        if not os.path.exists(FILE_NAME):
            messagebox.showerror("Error", "No data found")
            return

        df = pd.read_csv(FILE_NAME)

        if name in df["Name"].values:
            df = df[df["Name"] != name]
            df.to_csv(FILE_NAME, index=False)
            messagebox.showinfo("Success", "Patient Deleted")
        else:
            messagebox.showerror("Error", "Patient not found")

    # ------------------ View Patients ------------------

    def view_patients(self):
        if not os.path.exists(FILE_NAME):
            messagebox.showerror("Error", "No data found")
            return

        df = pd.read_csv(FILE_NAME)

        if df.empty:
            messagebox.showinfo("Info", "No patients available")
            return

        display_text = ""

        for _, row in df.iterrows():
            display_text += f"""
Name: {row['Name']}
Age: {row['Age']}
Avg BP: {row['Avg_BP']}
Avg Sugar: {row['Avg_Sugar']}
Risk: {row['Risk']}
Suggestion: {row['Suggestion']}
-----------------------------
"""

        window = tk.Toplevel(self.root)
        window.title("Patient Records")

        text_area = tk.Text(window, width=60, height=20)
        text_area.pack()

        text_area.insert(tk.END, display_text)
        text_area.config(state="disabled")

    # ------------------ Generate Report ------------------

    def generate_report(self):
        name = self.name.get()

        if not os.path.exists(FILE_NAME):
            messagebox.showerror("Error", "No data found")
            return

        df = pd.read_csv(FILE_NAME)

        if name not in df["Name"].values:
            messagebox.showerror("Error", "Patient not found")
            return

        patient = df[df["Name"] == name].iloc[0]

        report = f"""
==============================
        HEALTH REPORT
==============================

Name: {patient['Name']}
Age: {patient['Age']}

Average Blood Pressure: {patient['Avg_BP']}
Average Sugar Level: {patient['Avg_Sugar']:.2f}

Health Risk:
{patient['Risk']}

Doctor Suggestion:
{patient['Suggestion']}

------------------------------
Generated by AI Hospital System
------------------------------
"""

        file_name = f"{name}_report.txt"

        with open(file_name, "w") as f:
            f.write(report)

        messagebox.showinfo("Success", f"Report saved as {file_name}")

# ------------------ Run ------------------

root = tk.Tk()
app = HospitalSystem(root)
root.mainloop()