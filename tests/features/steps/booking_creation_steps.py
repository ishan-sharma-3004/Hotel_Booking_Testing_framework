from behave import given, when, then
from helpers.data_generator import DataGenerator
import time

@given('I have valid booking data')
def step_impl(context):
    context.booking_data = DataGenerator.generate_valid_booking_data()

@given('I have booking data with missing required fields')
def step_impl(context):
    context.booking_data = {'firstname': 'Test'}  # Minimal invalid data

@when('I create a new booking')
def step_impl(context):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            context.response = context.client.create_booking(context.booking_data)
            if context.response.status_code < 500:
                break
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)  # Wait before retrying