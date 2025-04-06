Feature: Booking Retrieval
  As a booking service client
  I want to retrieve booking information
  So I can view reservation details

  Scenario: Get existing booking
    Given I have an existing booking ID
    When I retrieve the booking details
    Then the response status should be 200
    And the booking details should be complete

  Scenario: Get non-existent booking
    Given I have an invalid booking ID
    When I retrieve the booking details
    Then the response status should be 404