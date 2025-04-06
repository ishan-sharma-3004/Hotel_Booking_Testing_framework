import pytest
import requests

from helpers.data_generator import DataGenerator


class TestAuthentication:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for the TestAuthentication class."""
        self.base_url = "https://restful-booker.herokuapp.com/auth"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.valid_credentials = DataGenerator.generate_valid_credentials()
        self.invalid_credentials = DataGenerator.generate_invalid_credentials()

    def test_token_generation(self):
        """Test token generation with valid credentials"""
        response = requests.post(
            self.base_url, headers=self.headers, json=self.valid_credentials
        )
        assert response.status_code == 200 or response.status_code == 201
        token_data = response.json()
        assert "token" in token_data
        assert len(token_data["token"]) > 0
        assert type(token_data["token"]) == str

    @pytest.mark.parametrize(
        "invalid_data",
        [
            {"username": "", "password": "password123"},
            {"username": "admin", "password": ""},
            {"username": "invalid", "password": "wrongpassword"},
            {"username": "", "password": ""},
        ],
    )
    def test_token_generation_with_invalid_credentials(self, invalid_data):
        """Test token generation with invalid credentials"""
        response = requests.post(self.base_url, headers=self.headers, json=invalid_data)

        assert response.status_code == 200
        token_data = response.json()
        assert "reason" in token_data
        assert "token" not in token_data
        assert token_data["reason"] == "Bad credentials"

    def test_token_generation_with_missing_field(self):
        """Test token generation with missing field"""
        response = requests.post(self.base_url, headers=self.headers, json={})

        assert response.status_code == 200
        token_data = response.json()
        assert "token" not in token_data
        assert "reason" in token_data
