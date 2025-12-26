import os
import httpx
import logging

logger = logging.getLogger(__name__)

class DIDService:
    def __init__(self):
        self.api_key = os.getenv("DID_API_KEY")
        self.base_url = "https://api.d-id.com"
        
    def _get_headers(self):
        import base64
        # Check if key needs encoding (contains colon and not obviously base64)
        if ":" in self.api_key:
            encoded_key = base64.b64encode(self.api_key.encode('utf-8')).decode('utf-8')
            auth_header = f"Basic {encoded_key}"
        else:
            # Assume user provided the full base64 string
            auth_header = f"Basic {self.api_key}"
            
        return {
            "Authorization": auth_header,
            "Content-Type": "application/json"
        }

    def _log_debug(self, msg):
        with open("did_debug.log", "a") as f:
            f.write(f"{msg}\n")

    async def create_stream(self, source_url: str):
        """
        Initialize a WebRTC stream with a source image.
        """
        self._log_debug(f"Creating stream for {source_url}...")
        if not self.api_key:
            self._log_debug("ERROR: D-ID API Key missing.")
            logger.error("D-ID API Key missing.")
            return None
            
        url = f"{self.base_url}/talks/streams"
        payload = {
            "source_url": source_url
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=self._get_headers())
                response.raise_for_status()
                data = response.json()
                self._log_debug(f"Stream Created: {data}")
                return data
            except Exception as e:
                self._log_debug(f"Failed to create stream: {e}")
                logger.error(f"Failed to create stream: {e}")
                return None

    async def send_script(self, stream_id: str, session_id: str, text: str):
        """
        Send text to the stream to make the avatar speak.
        """
        url = f"{self.base_url}/talks/streams/{stream_id}"
        payload = {
            "script": {
                "type": "text",
                "input": text,
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-US-GuyNeural" # Default voice, can be changed
                }
            },
            "session_id": session_id
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=self._get_headers())
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Failed to send script to stream: {e}")
                return None
    async def start_stream(self, stream_id: str, session_id: str, answer: dict):
        """
        Send the SDP Answer from the client to D-ID to start the WebRTC session.
        """
        url = f"{self.base_url}/talks/streams/{stream_id}/sdp"
        payload = {
            "answer": answer,
            "session_id": session_id
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=self._get_headers())
                response.raise_for_status()
                return True
            except Exception as e:
                logger.error(f"Failed to start stream (SDP exchange): {e}")
                return False

    async def submit_ice(self, stream_id: str, session_id: str, candidate: dict):
        """
        Submit an ICE candidate from the client to D-ID.
        """
        url = f"{self.base_url}/talks/streams/{stream_id}/ice"
        payload = {
            "candidate": candidate,
            "session_id": session_id
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=self._get_headers())
                response.raise_for_status()
                return True
            except Exception as e:
                logger.error(f"Failed to submit ICE candidate: {e}")
                return False
