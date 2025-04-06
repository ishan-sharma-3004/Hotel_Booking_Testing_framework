import pytest
import allure
import requests
from ..helpers.api_client import BookingAPIClient
from ..helpers.data_generator import DataGenerator
from ..helpers.self_healing import SelfHealing

class TestGetBooking:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.base_url = "https://restful-booker.herokuapp.com/booking"
        self.api_client = BookingAPIClient()
        self.api_client.authenticate()
        # Create a booking to test with
        self.booking_data = DataGenerator.generate_valid_booking_data()
        create_response = self.api_client.create_booking(self.booking_data)
        self.booking_id = create_response.json()["bookingid"]
        SelfHealing.store_booking_id(self.booking_id)

    @allure.feature("Booking")
    @allure.story("Get Booking")
    def test_get_existing_booking(self):
        """Test retrieving an existing booking"""
        with allure.step(f"Get booking with ID {self.booking_id}"):
            response = requests.get(f"{self.base_url}/{self.booking_id}")
        
        with allure.step("Verify booking details"):
            assert response.status_code == 200
            booking = response.json()
            assert booking["firstname"] == self.booking_data["firstname"]
            assert booking["lastname"] == self.booking_data["lastname"]
            assert booking["bookingdates"]["checkin"] == self.booking_data["bookingdates"]["checkin"]

    @allure.feature("Booking")
    @allure.story("Get Non-Existent Booking")
    def test_get_nonexistent_booking(self):
        """Test retrieving a booking that doesn't exist"""
        non_existent_id = 'fake_id'  # Assuming this ID doesn't exist
        
        with allure.step(f"Attempt to get booking with invalid ID {non_existent_id}"):
            response = requests.get(f"{self.base_url}/{non_existent_id}")
        
        with allure.step("Verify booking not found"):
            assert response.status_code == 404

    @allure.feature("Booking")
    @allure.story("Get Booking with Invalid ID")
    @pytest.mark.parametrize("invalid_id", [
        "invalid",   # String instead of number
        #"",          # Empty string
        "0",        # Zero ID
        "-1",       # Negative ID
        #"1.5"       # Float ID
    ])
    def test_get_booking_with_invalid_id(self, invalid_id):
        """Test retrieving a booking with invalid ID format"""
        with allure.step(f"Attempt to get booking with invalid ID format {invalid_id}"):
            response = requests.get(f"{self.base_url}/{invalid_id}")
        
        with allure.step("Verify invalid request"):
            # API returns 404 for invalid ID formats
            assert response.status_code == 404

    @allure.feature("Booking")
    @allure.story("Get All Bookings")
    def test_get_all_bookings(self):
        """Test retrieving all bookings"""
        with allure.step("Get all bookings"):
            response = requests.get(self.base_url)
        
        with allure.step("Verify response"):
            assert response.status_code == 200
            bookings = response.json()
            assert isinstance(bookings, list)
            assert len(bookings) > 0
            
            # Verify our test booking is in the list
            booking_ids = [b["bookingid"] for b in bookings]
            assert self.booking_id in booking_ids