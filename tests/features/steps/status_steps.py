# tests/features/steps/status_steps.py
from behave import then

@then('the response status should be {status_code:d}')
def step_impl(context, status_code):
    assert context.response.status_code == status_code, \
        f"Expected status {status_code}, got {context.response.status_code}"