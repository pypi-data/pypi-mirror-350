from typing import Dict, Any

class V2RX:
    """
    Client for interacting with V2RX (Ekascribe) session status APIs.
    This is typically used to fetch the results of an audio transcription job
    initiated via the file upload mechanism with action 'ekascribe'.
    """

    def __init__(self, client):
        """
        Initialize the V2RX client.

        Args:
            client: The EkaCareClient instance.
        """
        self.client = client

    def get_session_status(self, session_id: str, action="ekascribe") -> Dict[str, Any]:
        """
        Fetch the status and results of a voice recording session (Ekascribe job).

        After uploading an audio file for Ekascribe and receiving a webhook notification
        indicating completion, this method can be used to retrieve the transcription results.
        The `session_id` is typically part of the webhook payload.

        Args:
            session_id (str): The ID of the voice recording session.

        Returns:
            dict: A dictionary containing the session status information.
                  This includes the status of the job (e.g., "completed", "failed")
                  and, if successful, the output data, which often contains a
                  base64 encoded FHIR bundle.

        Raises:
            ValueError: If the session_id is null or empty.
            EkaCareAPIError: If the API call fails or returns an error status.

        Example:
            >>> # client is an instance of EkaCareClient
            >>> # session_id is obtained from the webhook after audio processing
            >>> status_response = client.v2rx.get_session_status("your_session_id_here")
            >>> print(f"Job Status: {status_response.get('status')}")
            >>> if status_response.get('status') == 'completed':
            ...     fhir_base64 = status_response.get('data', {}).get('output', {}).get('fhir')
            ...     if fhir_base64:
            ...         # Decode and process the FHIR data
            ...         pass
        """
        if not session_id:
            raise ValueError("Session ID cannot be null or empty")
        
        endpoint = f"/voice-record/api/status/{session_id}"
        
        if action == "ekascribe-v2":
            endpoint = f"voice/api/v3/status/{session_id}"

        return self.client.request(method="GET", endpoint=endpoint)