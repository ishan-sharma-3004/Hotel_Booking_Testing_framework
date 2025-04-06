from behave import *
from helpers.api_client import BookingAPIClient
from helpers.data_generator import *


@when("I update the booking with new details")
def step_impl(context):
    context.updated_data = context.original_data.copy()
    context.updated_data["firstname"] = "UpdatedName"
    context.response = context.client.update_booking(
        context.booking_id, context.updated_data
    )


@when("I partially update the booking with new additional needs")
def step_impl(context):
    context.partial_update = {"additionalneeds": "Breakfast Upgrade"}
    context.response = context.client.partial_update_booking(
        context.booking_id, context.partial_update
    )


@then("the booking should be successfully updated")
def step_impl(context):
    assert context.response.status_code == 200
    response = context.client.get_booking(context.booking_id)
    assert response.json()["firstname"] == "UpdatedName"


@then("only the specified fields should be updated")
def step_impl(context):
    response = context.client.get_booking(context.booking_id)
    booking = response.json()
    assert booking["additionalneeds"] == "Breakfast Upgrade"
    assert booking["firstname"] == context.original_data["firstname"]
