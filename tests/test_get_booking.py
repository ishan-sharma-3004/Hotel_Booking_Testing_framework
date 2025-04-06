import pytest
import requests

from helpers.api_client import BookingAPIClient
from helpers.data_generator import DataGenerator


class TestGetBooking:
    """Test class for getting a booking"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup method for the TestGetBooking class."""
        self.base_url = "https://restful-booker.herokuapp.com/booking"
        self.api_client = BookingAPIClient()
        self.api_client.authenticate()
        # Create a booking to test with
        self.booking_data = DataGenerator.generate_valid_booking_data()
        create_response = self.api_client.create_booking(self.booking_data)
        self.booking_id = create_response.json()["bookingid"]

    def test_get_existing_booking(self):
        """Test getting an existing booking"""
        response = requests.get(f"{self.base_url}/{self.booking_id}")

        assert response.status_code == 200
        booking = response.json()
        assert booking["firstname"] == self.booking_data["firstname"]
        assert booking["lastname"] == self.booking_data["lastname"]
        assert (
            booking["bookingdates"]["checkin"]
            == self.booking_data["bookingdates"]["checkin"]
        )

    def test_get_nonexistent_booking(self):
        """Test getting a non-existent booking"""
        non_existent_id = 999999  # Assuming this ID doesn't exist

        response = requests.get(f"{self.base_url}/{non_existent_id}")

        assert response.status_code == 404

    @pytest.mark.parametrize(
        "invalid_id",
        [
            "invalid",  # String instead of number
            # "",  # Empty string
            "0",  # Zero ID
            "-1",  # Negative ID
            # "1.5",  # Float ID
        ],
    )
    def test_get_booking_with_invalid_id(self, invalid_id):
        """Test getting a booking with invalid ID"""
        response = requests.get(f"{self.base_url}/{invalid_id}")

        # API returns 404 for invalid ID formats
        assert response.status_code == 404

    def test_get_all_bookings(self):
        """Test getting all bookings"""
        response = requests.get(self.base_url)

        assert response.status_code == 200
        bookings = response.json()
        assert isinstance(bookings, list)
        assert len(bookings) > 0

        # Verify our test booking is in the list
        booking_ids = [b["bookingid"] for b in bookings]
        assert self.booking_id in booking_ids
