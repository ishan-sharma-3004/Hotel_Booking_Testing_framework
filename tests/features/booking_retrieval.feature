Feature: Booking Retrieval
  As a booking manager
  I want to retrieve booking information
  So I can view reservation details

  Scenario: Get existing booking
    Given I have an existing booking
    When I retrieve the booking details
    Then the booking information should be returned
    And the details should match the created booking

  Scenario: Get non-existent booking
    Given I have a non-existent booking ID
    When I retrieve the booking details
    Then the request should fail with status code 404

  Scenario: Get all bookings
    Given there are existing bookings
    When I retrieve all bookings
    Then I should receive a list of bookings
    And my test booking should be in the list