from behave import then

@then('the response status should be {status_code:d}')
def step_impl(context, status_code):
    if hasattr(context, 'exception'):
        raise context.exception
    assert hasattr(context, 'response'), "No response in context"
    assert context.response.status_code == status_code, \
        f"Expected {status_code}, got {context.response.status_code}"