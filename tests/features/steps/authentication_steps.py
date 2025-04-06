from behave import *
from helpers.api_client import BookingAPIClient
from helpers.data_generator import DataGenerator


@given("I have valid admin credentials")
def stepImplementation(context):
    context.client = BookingAPIClient()


@given("I have invalid credentials")
def stepImplementation(context):
    context.client = BookingAPIClient(username="invalid", password="wrong")


@given("I have no credentials")
def stepImplementation(context):
    context.client = BookingAPIClient(username="", password="")


@when("I request an authentication token")
def stepImplementation(context):
    context.response = context.client.authenticate()


@then("I should receive a valid token")
def stepImplementation(context):
    assert context.response.status_code == 200
    assert "token" in context.response.json()


@then("I should receive an authentication error")
def stepImplementation(context):
    assert context.response.status_code == 200
    assert "reason" in context.response.json()
