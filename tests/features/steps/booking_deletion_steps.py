from behave import when, then

@when('I delete the booking')
def step_impl(context):
    context.response = context.client.delete_booking(
        context.booking_id,
        token=context.token
    )

@then('the booking should no longer exist')
def step_impl(context):
    response = context.client.get_booking(context.booking_id)
    assert response.status_code == 404, "Booking still exists"