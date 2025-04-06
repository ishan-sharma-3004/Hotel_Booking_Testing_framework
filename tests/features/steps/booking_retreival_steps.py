# tests/features/steps/booking_retreival_steps.py
from behave import given, when, then
from helpers.api_client import BookingAPIClient
from helpers.data_generator import DataGenerator
from booking_steps import *


@when("I retrieve the booking details")
def step_impl(context):
    context.response = context.client.get_booking(context.booking_id)


@then("the booking details should be complete")
def step_impl(context):
    booking = context.response.json()
    assert "firstname" in booking
    assert "lastname" in booking
    assert "totalprice" in booking
