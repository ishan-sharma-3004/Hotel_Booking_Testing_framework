from behave import *
from helpers.api_client import BookingAPIClient
from helpers.data_generator import DataGenerator


@given("I have a non-existent booking ID")
def step_impl(context):
    context.booking_id = 999999


@given("I am not authenticated")
def step_impl(context):
    context.client.token = None


@when("I delete the booking")
@when("I attempt to delete the booking")
def step_impl(context):
    context.response = context.client.delete_booking(context.booking_id)


@then("the booking should be successfully deleted")
def step_impl(context):
    assert context.response.status_code == 201


@then("the booking should no longer exist")
def step_impl(context):
    response = context.client.get_booking(context.booking_id)
    assert response.status_code == 404
