import pytest
import requests
import allure

from ..helpers.api_client import BookingAPIClient
from ..helpers.data_generator import DataGenerator
from ..helpers.self_healing import SelfHealing


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

    @allure.feature("Booking")
    @allure.story("Delete Booking")
    def test_delete_existing_booking(self):
        """Test deleting an existing booking"""
        with allure.step(f"Delete booking with ID {self.booking_id}"):
            response = requests.delete(
                f"{self.base_url}/{self.booking_id}", headers=self.headers
            )
        with allure.step("Verify deletion was successful"):
            assert response.status_code == 201

            # Verify booking is deleted
            get_response = requests.get(f"{self.base_url}/{self.booking_id}")
            assert get_response.status_code == 404

            #Self-healing: remove deleted booking ID
            SelfHealing.remove_booking_id(self.booking_id)

    @allure.feature("Booking")
    @allure.story("Deleting Booking Without Authentication")
    def test_delete_booking_without_auth(self):
        """Test deleting a booking without authentication"""
        with allure.step(f"Attempt to delete booking without auth headers"):
            response = requests.delete(
                f"{self.base_url}/{self.booking_id}",
                headers={"Content-Type": "application/json"},
            )

        with allure.step("Verify deletion failed"):
            assert response.status_code == 403  # Forbidden

            # Verify booking still exists
            get_response = requests.get(f"{self.base_url}/{self.booking_id}")
            assert get_response.status_code == 200

    @allure.feature("Booking")
    @allure.story("Delete Non-Existent Booking")
    def test_delete_nonexistent_booking(self):
        """Test deleting a non-existent booking"""
        non_existent_id = 999999

        with allure.step(f"Attempt to delete non-existent booking"):
            response = requests.delete(
                f"{self.base_url}/{non_existent_id}", headers=self.headers
            )

        with allure.step("Verify deletion failed"):  # with allure
            assert response.status_code == 405  # Method not allowed


    @allure.feature("Booking")
    @allure.story("Delete Already Deleted Booking")
    def test_delete_already_deleted_booking(self):
        """Test deleting a booking that has already been deleted"""
        # First delete the booking
        requests.delete(f"{self.base_url}/{self.booking_id}", headers=self.headers)

        with allure.step(f"Attempt to delete already deleted booking"):
            response = requests.delete(
                f"{self.base_url}/{self.booking_id}", headers=self.headers
            )

        with allure.step("Verify deletion failed"):
            assert response.status_code == 405  # Method not allowed
