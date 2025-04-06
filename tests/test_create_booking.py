from datetime import datetime, timedelta

import pytest
import requests

from helpers.data_generator import DataGenerator


class TestCreateBooking:
    """Test class for creating a booking."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup method for the TestCreateBooking class."""
        self.base_url = "https://restful-booker.herokuapp.com/booking"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def test_create_valid_booking(self):
        """Test creating a valid booking"""
        booking_data = DataGenerator.generate_valid_booking_data()

        response = requests.post(self.base_url, headers=self.headers, json=booking_data)

        assert response.status_code == 200
        response_data = response.json()
        assert "bookingid" in response_data
        assert isinstance(response_data["bookingid"], int)

        # Verify booking details in response
        booking = response_data["booking"]
        assert booking["firstname"] == booking_data["firstname"]
        assert booking["lastname"] == booking_data["lastname"]

    @pytest.mark.parametrize(
        "invalid_data",
        [
            DataGenerator.generate_booking_with_missing_firstname(),
            DataGenerator.generate_booking_with_missing_lastname(),
            # DataGenerator.generate_booking_with_invalid_dates(),
            DataGenerator.generate_booking_with_missing_dates(),
            DataGenerator.generate_empty_booking_data(),
        ],
    )
    def test_create_booking_with_invalid_data(self, invalid_data):
        """Test creating a booking with invalid data"""
        response = requests.post(self.base_url, headers=self.headers, json=invalid_data)

        assert response.status_code == 500

    @pytest.mark.parametrize(
        "edge_case_data",
        [
            DataGenerator.generate_booking_with_long_names(),
            DataGenerator.generate_booking_with_max_price(),
            DataGenerator.generate_booking_with_min_price(),
            DataGenerator.generate_booking_with_special_chars(),
        ],
    )
    def test_create_booking_with_edge_cases(self, edge_case_data):
        """Test creating a booking with edge cases"""
        response = requests.post(
            self.base_url, headers=self.headers, json=edge_case_data
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "bookingid" in response_data
        assert isinstance(response_data["bookingid"], int)
