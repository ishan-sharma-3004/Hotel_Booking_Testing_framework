import pytest
import requests
import allure
from ..helpers.data_generator import DataGenerator
from ..helpers.self_healing import SelfHealing

class TestAuthentication:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.base_url = "https://restful-booker.herokuapp.com/auth"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.valid_credentials = DataGenerator.generate_valid_credentials()
        self.invalid_credentials = DataGenerator.generate_invalid_credentials()

    @allure.feature("Authentication")
    @allure.story("Valid Authentication")
    def test_token_generation_with_valid_credentials(self):
        """Test token generation with valid credentials"""
        with allure.step("Generate token with valid credentials"):
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=self.valid_credentials
            )
        
        with allure.step("Verify response"):
            assert response.status_code == 200
            token_data = response.json()
            assert "token" in token_data
            assert len(token_data["token"]) > 0
            assert isinstance(token_data["token"], str)
            
            # Store token for self-healing
            SelfHealing.store_token(token_data["token"])

    @allure.feature("Authentication")
    @allure.story("Invalid Authentication")
    @pytest.mark.parametrize("invalid_data", [
        {"username": "", "password": "password123"},  # Empty username
        {"username": "admin", "password": ""},       # Empty password
        {"username": "", "password": ""},            # Both empty
        {"username": "invalid", "password": "wrong"} # Wrong credentials
    ])
    def test_token_generation_with_invalid_credentials(self, invalid_data):
        """Test token generation with invalid credentials"""
        with allure.step(f"Attempt authentication with invalid data: {invalid_data}"):
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=invalid_data
            )
        
        with allure.step("Verify authentication failed"):
            # Note: API returns 200 even for failed auth
            assert response.status_code == 200  
            token_data = response.json()
            assert "token" not in token_data
            assert "reason" in token_data
            assert token_data["reason"] == "Bad credentials"

    @allure.feature("Authentication")
    @allure.story("Missing Authentication Data")
    def test_token_generation_with_missing_fields(self):
        """Test token generation with missing required fields"""
        with allure.step("Attempt authentication with missing fields"):
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={}  # Empty payload
            )
        
        with allure.step("Verify authentication failed"):
            assert response.status_code == 200
            token_data = response.json()
            assert "token" not in token_data
            assert "reason" in token_data