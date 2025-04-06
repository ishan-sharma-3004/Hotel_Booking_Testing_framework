import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .self_healing import SelfHealing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BookingAPIClient:
    def __init__(self):
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.token = None
        self.token_expiry = None
        self.base_url = "https://restful-booker.herokuapp.com"

    def authenticate(self, auth_data):
        url = f"{self.base_url}/auth"
        try:
            response = self.session.post(
                url,
                json=auth_data,
                timeout=10,
                headers={"Content-Type": "application/json"},
            )
            return response
        except requests.exceptions.RequestException as e:
            print(f"Authentication failed: {str(e)}")
            return None

    def _attempt_self_healing(self) -> None:
        """Attempt to recover from previous session state"""
        stored_token = SelfHealing.get_token()
        if stored_token:
            self.token = stored_token
            logger.info("Recovered token from self-healing storage")

        stored_booking_ids = SelfHealing.get_booking_ids()
        if stored_booking_ids:
            logger.info(
                f"Found {len(stored_booking_ids)} booking IDs in self-healing storage"
            )

    def _is_token_valid(self) -> bool:
        """Check if the current token is still valid"""
        if not self.token or not self.token_expiry:
            return False
        return datetime.now() < self.token_expiry

    def authenticate(self, auth_data=None):
        """
        Authenticate and store token

        Args:
            auth_data: Optional dict containing username/password

        Returns:
            Response from authentication endpoint
        """
        if auth_data is None:
            auth_data = {"username": self.username, "password": self.password}

        url = f"{self.base_url}/auth"

        # Try to use self-healing token first if available
        if self._is_token_valid():
            logger.info("Using existing valid token")
            response = requests.Response()
            response.status_code = 200
            response._content = b'{"token":"' + self.token.encode() + b'"}'
            return response

        response = self.session.post(url, json=auth_data)

    def create_booking(self, booking_data: Dict[str, Any]) -> requests.Response:
        """
        Create a new booking

        Args:
            booking_data: Dictionary containing booking details

        Returns:
            Response from booking creation endpoint
        """
        url = f"{self.base_url}/booking"
        response = self.session.post(url, json=booking_data)

        if response.status_code == 200:
            booking_id = response.json().get("bookingid")
            if booking_id:
                SelfHealing.store_booking_id(booking_id)
                logger.info(f"Stored booking ID {booking_id} for self-healing")

        return response

    def get_booking(self, booking_id: int) -> requests.Response:
        """
        Get booking by ID

        Args:
            booking_id: ID of the booking to retrieve

        Returns:
            Response from booking retrieval endpoint
        """
        url = f"{self.base_url}/booking/{booking_id}"
        return self.session.get(url)

    def get_all_bookings(self) -> requests.Response:
        """
        Get all bookings

        Returns:
            Response from bookings endpoint
        """
        url = f"{self.base_url}/booking"
        return self.session.get(url)

    def update_booking(
        self, booking_id: int, booking_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Update an existing booking

        Args:
            booking_id: ID of the booking to update
            booking_data: Dictionary containing updated booking details

        Returns:
            Response from booking update endpoint
        """
        if not self._is_token_valid():
            self.authenticate()

        url = f"{self.base_url}/booking/{booking_id}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={self.token}",
            "Authorization": f"Bearer {self.token}",
        }
        return self.session.put(url, json=booking_data, headers=headers)

    def partial_update_booking(
        self, booking_id: int, update_fields: Dict[str, Any]
    ) -> requests.Response:
        """
        Partially update a booking (PATCH)

        Args:
            booking_id: ID of the booking to update
            update_fields: Dictionary containing fields to update

        Returns:
            Response from booking update endpoint
        """
        if not self._is_token_valid():
            self.authenticate()

        url = f"{self.base_url}/booking/{booking_id}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={self.token}",
            "Authorization": f"Bearer {self.token}",
        }
        return self.session.patch(url, json=update_fields, headers=headers)

    def delete_booking(self, booking_id: int) -> requests.Response:
        """
        Delete a booking

        Args:
            booking_id: ID of the booking to delete

        Returns:
            Response from booking deletion endpoint
        """
        if not self._is_token_valid():
            self.authenticate()

        url = f"{self.base_url}/booking/{booking_id}"
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"token={self.token}",
            "Authorization": f"Bearer {self.token}",
        }
        response = self.session.delete(url, headers=headers)

        if response.status_code == 201:
            SelfHealing.remove_booking_id(booking_id)
            logger.info(f"Removed booking ID {booking_id} from self-healing storage")

        return response

    def health_check(self) -> requests.Response:
        """
        Perform a health check on the API

        Returns:
            Response from ping endpoint
        """
        url = f"{self.base_url}/ping"
        return self.session.get(url)

    def cleanup_test_data(self):
        """
        Clean up any test data that was created
        """
        booking_ids = SelfHealing.get_booking_ids()
        for booking_id in booking_ids:
            try:
                self.delete_booking(booking_id)
            except Exception as e:
                logger.warning(f"Failed to delete booking {booking_id}: {str(e)}")

        SelfHealing.cleanup_test_data()
        logger.info("Cleaned up all test data")
