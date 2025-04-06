import pytest
import allure
import requests
from datetime import datetime, timedelta
from ..helpers.data_generator import DataGenerator
from ..helpers.self_healing import SelfHealing

class TestCreateBooking:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.base_url = "https://restful-booker.herokuapp.com/booking"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @allure.feature("Booking")
    @allure.story("Create Booking")
    def test_create_valid_booking(self):
        """Test creating a booking with valid data"""
        booking_data = DataGenerator.generate_valid_booking_data()
        
        with allure.step("Create booking with valid data"):
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=booking_data
            )
        
        with allure.step("Verify booking creation"):
            assert response.status_code == 200
            response_data = response.json()
            assert "bookingid" in response_data
            assert isinstance(response_data["bookingid"], int)
            
            # Store booking ID for self-healing
            SelfHealing.store_booking_id(response_data["bookingid"])
            
            # Verify booking details in response
            booking = response_data["booking"]
            assert booking["firstname"] == booking_data["firstname"]
            assert booking["lastname"] == booking_data["lastname"]

    @allure.feature("Booking")
    @allure.story("Create Booking with Invalid Data")
    @pytest.mark.parametrize("invalid_data", [
        DataGenerator.generate_booking_with_missing_firstname(),
        DataGenerator.generate_booking_with_missing_lastname(),
        #DataGenerator.generate_booking_with_invalid_dates(),
        DataGenerator.generate_booking_with_missing_dates(),
        DataGenerator.generate_empty_booking_data()
    ])
    def test_create_booking_with_invalid_data(self, invalid_data):
        """Test creating a booking with invalid data"""
        with allure.step(f"Attempt to create booking with invalid data: {invalid_data}"):
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=invalid_data
            )
        
        with allure.step("Verify booking creation failed"):
            assert response.status_code == 500  # API returns 500 for invalid data

    @allure.feature("Booking")
    @allure.story("Create Booking with Edge Cases")
    @pytest.mark.parametrize("edge_case_data", [
        DataGenerator.generate_booking_with_long_names(),
        DataGenerator.generate_booking_with_max_price(),
        DataGenerator.generate_booking_with_min_price(),
        DataGenerator.generate_booking_with_special_chars()
    ])
    def test_create_booking_with_edge_cases(self, edge_case_data):
        """Test creating a booking with edge case data"""
        with allure.step(f"Create booking with edge case data: {edge_case_data}"):
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=edge_case_data
            )
        
        with allure.step("Verify booking creation"):
            assert response.status_code == 200
            response_data = response.json()
            assert "bookingid" in response_data
            
            # Store booking ID for self-healing
            SelfHealing.store_booking_id(response_data["bookingid"])