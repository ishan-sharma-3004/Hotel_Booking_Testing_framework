Feature: Booking Deletion

    As a userAs a booking admin
    I want to delete bookings
    So I can manage booking availability

    Scenario: Delete an existing booking 
        Given I have an existing booking
        When I delete the booking
        Then the booking should be successfully deleted
        And the booking should no longer exist
    
    Scenario: Delete a non-existing booking
        Given I have a non-existent booking ID
        When I attempt to delete the booking
        Then the request should fail with status code 405
    
    Scenario: Delete without authentication
        Given I have an existing booking    
        And I am not authenticated
        When I attempt to delete the booking
        Then the request should fail with status code 403
    
    