import pytest
import requests

from helpers.api_client import BookingAPIClient
from helpers.data_generator import DataGenerator


class TestDeleteBooking:
    """Test class for deleting a booking"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup method for the TestDeleteBooking class"""
        self.base_url = "https://restful-booker.herokuapp.com/booking"
        self.api_client = BookingAPIClient()
        self.api_client.authenticate()
        # Create a booking to test with
        self.booking_data = DataGenerator.generate_valid_booking_data()
        create_response = self.api_client.create_booking(self.booking_data)
        self.booking_id = create_response.json()["bookingid"]

        # Prepare headers with auth token
        self.headers = {
            "Content-Type": "application/json",
            "Cookie": f"token={self.api_client.token}",
            "Authorization": f"Bearer {self.api_client.token}",
        }

    def test_delete_existing_booking(self):
        """Test deleting an existing booking"""
        response = requests.delete(
            f"{self.base_url}/{self.booking_id}", headers=self.headers
        )

        assert response.status_code == 201

        # Verify booking is deleted
        get_response = requests.get(f"{self.base_url}/{self.booking_id}")
        assert get_response.status_code == 404

        # Self-healing: remove deleted booking ID
        # SelfHealing.remove_booking_id(self.booking_id)

    def test_delete_booking_without_auth(self):
        """Test deleting a booking without authentication"""
        response = requests.delete(
            f"{self.base_url}/{self.booking_id}",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 403  # Forbidden

        # Verify booking still exists
        get_response = requests.get(f"{self.base_url}/{self.booking_id}")
        assert get_response.status_code == 200

    def test_delete_nonexistent_booking(self):
        """Test deleting a non-existent booking"""
        non_existent_id = 999999

        response = requests.delete(
            f"{self.base_url}/{non_existent_id}", headers=self.headers
        )

        assert response.status_code == 405  # Method not allowed

    def test_delete_already_deleted_booking(self):
        """Test deleting a booking that has already been deleted"""
        # First delete the booking
        requests.delete(f"{self.base_url}/{self.booking_id}", headers=self.headers)

        response = requests.delete(
            f"{self.base_url}/{self.booking_id}", headers=self.headers
        )

        assert response.status_code == 405  # Method not allowed
