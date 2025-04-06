from behave import given, when, then
import json

@given('I have valid admin credentials')
def step_impl(context):
    context.auth_data = {
        'username': 'admin',
        'password': 'password123'  # Replace with actual valid credentials
    }

@given('I have invalid credentials')
def step_impl(context):
    context.auth_data = {
        'username': 'invalid',
        'password': 'wrongpassword'
    }

@when('I request an authentication token')
def step_impl(context):
    try:
        context.response = context.client.authenticate(context.auth_data)
        assert context.response is not None, "Authentication returned None"
    except Exception as e:
        context.exception = e

@then('I should receive a valid token')
def step_impl(context):
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    assert 'token' in context.response.json(), "No token in response"
    context.token = context.response.json()['token']