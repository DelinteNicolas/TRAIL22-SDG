Feature: Negation
    I want the model to understand negation

Scenario Outline: [DIR] When I negate a sentence, the model should not assign a SDG
    Given I input "<text>"
    When I negate as "<negation>"
    Then SDG <n> should be part of the initial SDGs assigned
    And SDG <n> should not be part of the final SDGs assigned

    Examples:
        | text | negation | n |
        | Our goal is to create inclusive, secure, resilient, and sustainable cities | Our goal is not to create inclusive, secure, resilient, and sustainable cities | 11 |
        