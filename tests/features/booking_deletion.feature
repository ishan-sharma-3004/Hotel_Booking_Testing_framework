Feature: Booking Deletion
  As a booking service client
  I want to delete bookings
  So I can cancel reservations

  Scenario: Delete an existing booking
    Given I have an existing booking ID
    When I delete the booking
    Then the response status should be 201
    And the booking should no longer exist

  Scenario: Delete already deleted booking
    Given I have a previously deleted booking ID
    When I delete the booking
    Then the response status should be 405