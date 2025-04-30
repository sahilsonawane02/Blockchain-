import streamlit as st
import hashlib

class DoctorAppointmentSystem:
    def __init__(self):
        self.appointments = {}  # In-memory storage for appointments
        self.doctors = set()    # Set to store doctors
        self.patients = set()   # Set to store patients

    def _hash_string(self, input_string):
        """Create a hash of a string using SHA-256."""
        return hashlib.sha256(input_string.encode('utf-8')).hexdigest()

    def add_doctor(self, doctor_name):
        """Add a doctor to the system."""
        hashed_doctor_name = self._hash_string(doctor_name)
        self.doctors.add(hashed_doctor_name)
        return f"Doctor {doctor_name} added."

    def remove_doctor(self, doctor_name):
        """Remove a doctor from the system."""
        hashed_doctor_name = self._hash_string(doctor_name)
        if hashed_doctor_name in self.doctors:
            self.doctors.remove(hashed_doctor_name)
            return f"Doctor {doctor_name} removed."
        else:
            return f"Doctor {doctor_name} not found."

    def book_appointment(self, patient_name, doctor_name, appointment_time):
        """Book an appointment."""
        hashed_doctor_name = self._hash_string(doctor_name)
        if hashed_doctor_name not in self.doctors:
            return f"Doctor {doctor_name} not found."
        
        if patient_name in self.patients:
            return f"Patient {patient_name} has already booked an appointment."
        
        # Create a unique appointment ID by hashing the patient name, doctor name, and appointment time
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
        """Confirm an appointment by the doctor."""
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
        """Cancel an appointment."""
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
        """View all appointments."""
        if self.appointments:
            appointments_list = []
            for appointment_id, details in self.appointments.items():
                appointments_list.append(f"ID: {appointment_id}, Patient: {details['patient']}, Doctor: {details['doctor']}, Time: {details['appointment_time']}, Status: {details['status']}")
            return "\n".join(appointments_list)
        else:
            return "No appointments found."

# Streamlit UI
st.title("Doctor Appointment System")

system = DoctorAppointmentSystem()

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose an action", ["Book Appointment", "View Appointments", "Manage Doctors"])

if option == "Book Appointment":
    st.header("Book an Appointment")
    patient_name = st.text_input("Enter your name:")
    doctor_name = st.text_input("Enter doctor's name:")
    appointment_time = st.text_input("Enter appointment time (e.g., 2025-05-01 10:00):")
    
    if st.button("Book Appointment"):
        if patient_name and doctor_name and appointment_time:
            result = system.book_appointment(patient_name, doctor_name, appointment_time)
            st.success(result)
        else:
            st.error("Please fill in all fields.")

elif option == "View Appointments":
    st.header("All Appointments")
    appointments = system.view_appointments()
    st.text(appointments)

elif option == "Manage Doctors":
    st.header("Manage Doctors")
    doctor_name = st.text_input("Enter doctor's name:")
    
    doctor_action = st.selectbox("Choose an action", ["Add Doctor", "Remove Doctor"])

    if doctor_action == "Add Doctor":
        if st.button("Add Doctor"):
            if doctor_name:
                result = system.add_doctor(doctor_name)
                st.success(result)
            else:
                st.error("Please enter a doctor's name.")

    elif doctor_action == "Remove Doctor":
        if st.button("Remove Doctor"):
            if doctor_name:
                result = system.remove_doctor(doctor_name)
                st.success(result)
            else:
                st.error("Please enter a doctor's name.")


