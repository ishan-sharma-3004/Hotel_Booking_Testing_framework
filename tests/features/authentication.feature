Feature: API Authentication
    As an API client
    I want to authenticate with the system
    So I can access protected endpoints

    Scenario: Successful Authentication
        Given I have a valid admin credentials
        When I request an authentication token
        Then I should receive a valid token
    
    Scenario: Failed Authentication
        Given I have invalid credentials
        When I request an authentication token
        Then I should receive an authentication error
    
    Scenario: Authentication with missing credentials
        Given I have missing credentials
        When I request an authentication token
        Then I should receive a bad credentials error
    
    