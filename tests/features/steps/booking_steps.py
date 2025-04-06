# booking_steps.py (new file)
from behave import given
from helpers.api_client import BookingAPIClient
from helpers.data_generator import DataGenerator


@given("I have an existing booking ID")
def step_impl(context):
    if not hasattr(context, "client"):
        context.client = BookingAPIClient()
    booking_data = DataGenerator.generate_valid_booking_data()
    response = context.client.create_booking(booking_data)
    context.booking_id = response.json()["bookingid"]
