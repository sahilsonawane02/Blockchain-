pip install streamlit
import streamlit as st
import uuid
import time

class DoctorAppointmentSystem:
    def __init__(self):
        self.appointments = {}  # In-memory storage for appointments
        self.doctors = set()    # Set to store doctors
        self.patients = set()   # Set to store patients

    def add_doctor(self, doctor_name):
        """Add a doctor to the system."""
        self.doctors.add(doctor_name)

    def remove_doctor(self, doctor_name):
        """Remove a doctor from the system."""
        if doctor_name in self.doctors:
            self.doctors.remove(doctor_name)

    def book_appointment(self, patient_name, doctor_name, appointment_time):
        """Book an appointment."""
        if doctor_name not in self.doctors:
            return "Doctor not found."
        if patient_name in self.patients:
            return "Patient has already booked an appointment."
        
        # Create a unique appointment ID
        appointment_id = str(uuid.uuid4())
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
        return "Appointment not found."

    def cancel_appointment(self, appointment_id):
        """Cancel an appointment."""
        if appointment_id in self.appointments:
            appointment = self.appointments[appointment_id]
            if appointment['status'] == 'Booked':
                appointment['status'] = 'Canceled'
                return f"Appointment {appointment_id} canceled."
            else:
                return f"Appointment {appointment_id} is already confirmed or canceled."
        return "Appointment not found."

    def view_appointments(self):
        """View all appointments."""
        if self.appointments:
            return self.appointments
        return "No appointments found."

# Create an instance of the appointment system
system = DoctorAppointmentSystem()

# Add doctors to the system
system.add_doctor("Dr. Smith")
system.add_doctor("Dr. Johnson")

# Streamlit user interface
st.title("Doctor Appointment Booking System")

# Book Appointment Section
st.header("Book an Appointment")
patient_name = st.text_input("Enter your name:")
doctor_name = st.selectbox("Select a doctor:", list(system.doctors))
appointment_time = st.text_input("Enter appointment time (YYYY-MM-DD HH:MM):")

if st.button("Book Appointment"):
    if patient_name and doctor_name and appointment_time:
        result = system.book_appointment(patient_name, doctor_name, appointment_time)
        st.success(result)
    else:
        st.error("Please fill in all fields.")

# View All Appointments Section
st.header("View All Appointments")
appointments = system.view_appointments()
if appointments != "No appointments found.":
    for appointment_id, details in appointments.items():
        st.write(f"ID: {appointment_id}, Patient: {details['patient']}, Doctor: {details['doctor']}, Time: {details['appointment_time']}, Status: {details['status']}")
else:
    st.write(appointments)

# Confirm Appointment Section
st.header("Confirm an Appointment")
appointment_id_to_confirm = st.text_input("Enter appointment ID to confirm:")
if st.button("Confirm Appointment"):
    if appointment_id_to_confirm:
        confirmation_result = system.confirm_appointment(appointment_id_to_confirm)
        st.success(confirmation_result)
    else:
        st.error("Please enter an appointment ID.")

# Cancel Appointment Section
st.header("Cancel an Appointment")
appointment_id_to_cancel = st.text_input("Enter appointment ID to cancel:")
if st.button("Cancel Appointment"):
    if appointment_id_to_cancel:
        cancellation_result = system.cancel_appointment(appointment_id_to_cancel)
        st.success(cancellation_result)
    else:
        st.error("Please enter an appointment ID.")

