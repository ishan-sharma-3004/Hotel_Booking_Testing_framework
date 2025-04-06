Feature: Booking Update
  As a booking service client
  I want to update bookings
  So I can modify reservation details

  Scenario: Update booking with valid data
    Given I have an existing booking ID
    And I have valid update data
    When I update the booking
    Then the response status should be 200
    And the booking should reflect the changes

  Scenario: Update booking without authentication
    Given I have an existing booking ID
    And I have valid update data
    But I am not authenticated
    When I update the booking
    Then the response status should be 403