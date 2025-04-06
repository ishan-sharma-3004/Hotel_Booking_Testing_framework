from behave import *
from helpers.api_client import BookingAPIClient
from helpers.data_generator import DataGenerator


@given("there are existing bookings")
def step_impl(context):
    context.client = BookingAPIClient()
    booking_data = DataGenerator.generate_valid_booking_data()
    response = context.client.create_booking(booking_data)
    context.booking_id = response.json()["bookingid"]


@when("I retrieve the booking details")
def step_impl(context):
    context.response = context.client.get_booking(context.booking_id)


@when("I retrieve all bookings")
def step_impl(context):
    context.response = context.client.get_all_bookings()


@then("the booking information should be returned")
def step_impl(context):
    assert context.response.status_code == 200
    assert "firstname" in context.response.json()


@then("my test booking should be in the list")
def step_impl(context):
    bookings = context.response.json()
    assert any(b["bookingid"] == context.booking_id for b in bookings)
