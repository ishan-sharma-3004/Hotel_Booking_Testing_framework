from behave import given, then

@then('the response should contain a booking ID')
def step_impl(context):
    assert hasattr(context, 'response'), "No response in context"
    assert 'bookingid' in context.response.json(), "No booking ID in response"

@given('I have an invalid booking ID')
def step_impl(context):
    context.booking_id = "invalid_id_123"

@then('the booking should reflect the changes')
def step_impl(context):
    response = context.client.get_booking(context.booking_id)
    booking = response.json()
    for key, value in context.update_data.items():
        assert booking[key] == value, f"{key} not updated correctly"