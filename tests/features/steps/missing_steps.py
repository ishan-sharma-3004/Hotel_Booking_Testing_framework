from behave import given, when, then
from helpers.data_generator import DataGenerator

@given('I have a previously deleted booking ID')
def step_impl(context):
    # Create and then delete a booking
    booking_data = DataGenerator.generate_valid_booking_data()
    response = context.client.create_booking(booking_data)
    booking_id = response.json()["bookingid"]
    context.client.delete_booking(booking_id)
    context.booking_id = booking_id

@given('I have valid update data')
def step_impl(context):
    context.update_data = {
        "firstname": "UpdatedName",
        "totalprice": 999
    }

@when('I update the booking')
def step_impl(context):
    context.response = context.client.update_booking(
        context.booking_id,
        context.update_data,
        token=context.token
    )

@given('I am not authenticated')
def step_impl(context):
    context.token = None  # Explicitly clear any existing token