Feature: API Authentication
  As an API client
  I want to authenticate with the system
  So I can access protected endpoints

  Scenario: Successful authentication with valid credentials
    Given I have valid admin credentials
    When I request an authentication token
    Then I should receive a valid token
    And the response status should be 200

  Scenario: Failed authentication with invalid credentials
    Given I have invalid credentials
    When I request an authentication token
    Then I should receive a 401 unauthorized error