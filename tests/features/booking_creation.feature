Feature: Booking Creation
  As a booking service client
  I want to create bookings
  So I can reserve resources

  Scenario: Create a valid booking
    Given I have valid booking data
    When I create a new booking
    Then the response status should be 200
    And the response should contain a booking ID

  Scenario: Create booking with invalid data
    Given I have booking data with missing required fields
    When I create a new booking
    Then the response status should be 500