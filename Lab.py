import streamlit as st
import hashlib

class DoctorAppointmentSystem:
    def __init__(self):
        self.appointments = {}  # In-memory storage for appointments
        self.doctors = set()    # Set to store doctors
        self.patients = set()   # Set to store patients

    def _hash_string(self, input_string):
        return hashlib.sha256(input_string.encode('utf-8')).hexdigest()

    def add_doctor(self, doctor_name):
        hashed_doctor_name = self._hash_string(doctor_name)
        self.doctors.add(hashed_doctor_name)
        return f"Doctor {doctor_name} added."

    def remove_doctor(self, doctor_name):
        hashed_doctor_name = self._hash_string(doctor_name)
        if hashed_doctor_name in self.doctors:
            self.doctors.remove(hashed_doctor_name)
            return f"Doctor {doctor_name} removed."
        else:
            return f"Doctor {doctor_name} not found."

    def book_appointment(self, patient_name, doctor_name, appointment_time):
        hashed_doctor_name = self._hash_string(doctor_name)
        if hashed_doctor_name not in self.doctors:
            return f"Doctor {doctor_name} not found."

        if patient_name in self.patients:
            return f"Patient {patient_name} has already booked an appointment."

        raw_appointment_id = patient_name + doctor_name + appointment_time
        appointment_id = self._hash_string(raw_appointment_id)

        self.appointments[appointment_id] = {
            'patient': patient_name,
            'doctor': doctor_name,
            'appointment_time': appointment_time,
            'status': 'Booked'
        }
        self.patients.add(patient_name)
        return f"Appointment booked: {appointment_id} for {patient_name} with Dr. {doctor_name} at {appointment_time}."

    def confirm_appointment(self, appointment_id):
        if appointment_id in self.appointments:
            appointment = self.appointments[appointment_id]
            if appointment['status'] == 'Booked':
                appointment['status'] = 'Confirmed'
                return f"Appointment {appointment_id} confirmed."
            else:
                return f"Appointment {appointment_id} is already confirmed or canceled."
        else:
            return f"Appointment {appointment_id} not found."

    def cancel_appointment(self, appointment_id):
        if appointment_id in self.appointments:
            appointment = self.appointments[appointment_id]
            if appointment['status'] == 'Booked':
                appointment['status'] = 'Canceled'
                return f"Appointment {appointment_id} canceled."
            else:
                return f"Appointment {appointment_id} is already confirmed or canceled."
        else:
            return f"Appointment {appointment_id} not found."

    def view_appointments(self):
        if self.appointments:
            return [
                f"ID: {aid}, Patient: {a['patient']}, Doctor: {a['doctor']}, Time: {a['appointment_time']}, Status: {a['status']}"
                for aid, a in self.appointments.items()
            ]
        else:
            return ["No appointments found."]

# Streamlit part starts here
st.title("Doctor Appointment System")

# Persist system state across Streamlit reruns
if 'system' not in st.session_state:
    st.session_state.system = DoctorAppointmentSystem()

system = st.session_state.system



