from behave import *
from helpers.api_client import BookingAPIClient

def before_scenario(context, scenario):
    context.client = BookingAPIClient()