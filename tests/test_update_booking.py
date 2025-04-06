import pytest
import requests

from helpers.api_client import BookingAPIClient
from helpers.data_generator import DataGenerator


class TestUpdateBooking:
    """Test class for updating a booking"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup method for the TestUpdateBooking class."""
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
            "Accept": "application/json",
            "Cookie": f"token={self.api_client.token}",
            "Authorization": f"Bearer {self.api_client.token}",
        }

    def test_update_existing_booking(self):
        """Test updating an existing booking"""
        updated_data = self.booking_data.copy()
        updated_data["firstname"] = "UpdatedName"
        updated_data["additionalneeds"] = "Lunch"

        response = requests.put(
            f"{self.base_url}/{self.booking_id}",
            headers=self.headers,
            json=updated_data,
        )

        assert response.status_code == 200

        # Verify changes
        get_response = requests.get(f"{self.base_url}/{self.booking_id}")
        updated_booking = get_response.json()
        assert updated_booking["firstname"] == "UpdatedName"
        assert updated_booking["additionalneeds"] == "Lunch"

    def test_update_booking_with_invalid_data(self):
        """Test updating a booking with invalid data"""
        invalid_data = {"firstname": ""}  # Empty firstname

        response = requests.put(
            f"{self.base_url}/{self.booking_id}",
            headers=self.headers,
            json=invalid_data,
        )

        assert response.status_code == 400  # Bad request

    def test_update_booking_without_auth(self):
        """Test updating a booking without authentication"""
        updated_data = self.booking_data.copy()
        updated_data["firstname"] = "ShouldNotUpdate"

        response = requests.put(
            f"{self.base_url}/{self.booking_id}",
            headers={"Content-Type": "application/json"},
            json=updated_data,
        )

        assert response.status_code == 403  # Forbidden

    def test_update_nonexistent_booking(self):
        """Test updating a non-existent booking"""
        non_existent_id = 999999
        updated_data = self.booking_data.copy()

        response = requests.put(
            f"{self.base_url}/{non_existent_id}",
            headers=self.headers,
            json=updated_data,
        )

        assert response.status_code == 405  # Method not allowed
