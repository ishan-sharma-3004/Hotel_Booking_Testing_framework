from behave import given, when, then

@given("I have valid admin credentials")
def step_impl(context):
    context.auth_data = {
        "username": "admin",
        "password": "password123"
    }

@given("I have invalid credentials")
def step_impl(context):
    context.auth_data = {
        "username": "invalid",
        "password": "wrongpassword"
    }

@when("I request an authentication token")
def step_impl(context):
    context.response = context.client.authenticate(context.auth_data)

@then("I should receive a valid token")
def step_impl(context):
    assert context.response.status_code == 200, \
        f"Expected 200, got {context.response.status_code}"
    response_json = context.response.json()
    assert 'token' in response_json, "No token in response"
    context.token = response_json['token']