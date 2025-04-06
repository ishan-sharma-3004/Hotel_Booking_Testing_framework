from behave import *
from helpers.api_client import BookingAPIClient
from helpers.data_generator import DataGenerator


@given("I have valid booking data for {room_type}")
def step_impl(context, room_type):
    context.booking_data = DataGenerator.generate_valid_booking_data()
    context.booking_data["additionalneeds"] = room_type


@given("I have booking data with missing required fields")
def step_impl(context):
    context.booking_data = {"firstname": "Test"}


@when("I create a new booking")
def step_impl(context):
    context.client = BookingAPIClient()
    context.response = context.client.create_booking(context.booking_data)


@then("the booking should be created successfully")
def step_impl(context):
    assert context.response.status_code == 200
    context.booking_id = context.response.json()["bookingid"]


@then("the response should contain booking details")
def step_impl(context):
    booking = context.response.json()["booking"]
    assert booking["firstname"] == context.booking_data["firstname"]
