import pytest
import requests
import allure
from ..helpers.api_client import BookingAPIClient
from ..helpers.data_generator import DataGenerator
from ..helpers.self_healing import SelfHealing


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

    @allure.feature("Booking")
    @allure.story("Update Booking")
    def test_update_existing_booking(self):
        """Test updating an existing booking"""
        updated_data = self.booking_data.copy()
        updated_data["firstname"] = "UpdatedName"
        updated_data["additionalneeds"] = "Lunch"
        
        with allure.step(f"Update booking with ID {self.booking_id}"):
            response = requests.put(
                f"{self.base_url}/{self.booking_id}",
                headers=self.headers,
                json=updated_data,
            )
        
        with allure.step("verify update was successful"):
            assert response.status_code == 200

            # Verify changes
            get_response = requests.get(f"{self.base_url}/{self.booking_id}")
            updated_booking = get_response.json()
            assert updated_booking["firstname"] == "UpdatedName"
            assert updated_booking["additionalneeds"] == "Lunch"

    @allure.feature("Booking")
    @allure.story("Update Booking with Invalid Data")
    def test_update_booking_with_invalid_data(self):
        """Test updating a booking with invalid data"""
        invalid_data = {"firstname": ""}  # Empty firstname

        with allure.step(f"Attempt to update booking with invalid data"):
            response = requests.put(
                f"{self.base_url}/{self.booking_id}",
                headers=self.headers,
                json=invalid_data,
            )

        with allure.step("Verify update failed"):
            # Verify update failed
            assert response.status_code == 400  # Bad request

    @allure.feature("Booking")
    @allure.story("Update Booking Without Authentication")
    def test_update_booking_without_auth(self):
        """Test updating a booking without authentication"""
        updated_data = self.booking_data.copy()
        updated_data["firstname"] = "ShouldNotUpdate"

        with allure.step(f"Attempt to update booking without auth headers"):
            response = requests.put(
                f"{self.base_url}/{self.booking_id}",
                headers={"Content-Type": "application/json"},
                json=updated_data,
            )
        
        with allure.step("Verify update failed"):
            assert response.status_code == 403  # Forbidden

    @allure.feature("Booking")
    @allure.story("Update Non-Existent Booking")
    def test_update_nonexistent_booking(self):
        """Test updating a non-existent booking"""
        non_existent_id = 999999
        updated_data = self.booking_data.copy()

        with allure.step(f"Attempt to update non-existent booking"):
            response = requests.put(
                f"{self.base_url}/{non_existent_id}",
                headers=self.headers,
                json=updated_data,
            )

        with allure.step("Verify update failed"):
            assert response.status_code == 405  # Method not allowed
