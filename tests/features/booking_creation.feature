Feature: Booking Creation
    As a booking manager
    I want to create new bookings
    So that customers can reserve rooms

    Scenario: Create valid Booking
        Given I have a valid booking data
        When I create a new booking
        Then the booking should be created successfully
        And the response should contain booking details
    
    Scenario: Create booking with invalid data
        Given I have a booking data with missing required fields
        When I create a new booking
        Then the request should fail with status code 500