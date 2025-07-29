from typing import Dict, Any


class AppointmentWebhook:
    """Client for interacting with Eka Appointment Webhooks"""

    def __init__(self, client):
        self.client = client

    def get_detailed_appointment_data(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch the details of a specific appointment.

        Args:
            payload (dict): The payload received from the webhook

        Returns:
            dict: Detailed appointment data
        """
        appointment_id = payload.get("data", {}).get("appointment_id")
        patient_id = payload.get("data", {}).get("patient_id")
        clinic_id = payload.get("data", {}).get("clinic_id")
        doctor_id = payload.get("data", {}).get("doctor_id")

        if not appointment_id:
            raise ValueError("Missing appointment_id in payload")
        if not patient_id:
            raise ValueError("Missing patient_id in payload")
        if not clinic_id:
            raise ValueError("Missing clinic_id in payload")
        if not doctor_id:
            raise ValueError("Missing doctor_id in payload")

        appointment_details = self.client.appointments.get_appointment_details(
            appointment_id)
        appointment_details["rescheduled"] = False
        old_aid = payload.get("data", {}).get("p_aid")
        if old_aid and isinstance(old_aid, str):
            appointment_details["rescheduled"] = True
            appointment_details["old_appointment_details"] = self.client.appointments.get_appointment_details(
                old_aid)

        return {
            "appointment_details": appointment_details,
            "patient_details": self.client.patient.get_patient(patient_id),
            "clinic_details": self.client.clinic_doctor.get_clinic_details(clinic_id),
            "doctor_details": self.client.clinic_doctor.get_doctor_details(doctor_id)
        }
