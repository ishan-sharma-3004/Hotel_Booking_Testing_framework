Feature: Booking Update
    As a booking admin
    I want to update existing bookings
    So I can modify reservation details

    Scenario: Update booking details
        Given I have an existing booking
        When I update the booking with new details
        Then the booking should be successfully updated
        And the changes should be visible when retreived
    
    Scenario: Partial update of booking details
        Given I have an existing booking
        when I partially update the booking with new additional needs
        Then only the specified fields should be updated
    
    Scenario: Update without authentication
        Given I have an existing booking
        And I am not authenticated
        When I attemp to update the booking
        Then the request should fail with status code 403
    
    