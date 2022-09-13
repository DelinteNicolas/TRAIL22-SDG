Feature: Negation
    I want the model to understand negation
    So that it do not assign a SDG to a sentence that is not a SDG

Scenario Outline: [DIR] When I negate a sentence, the model should not assign a SDG
    Given I input "<text>"
    When I input "<negated_text>"
    Then SDG <n> should not be in the assigned SDGs anymore

    Examples:
        | text | negated_text | n |
        | Our goal is to create inclusive, secure, resilient, and sustainable cities | Our goal is not to create inclusive, secure, resilient, and sustainable cities | 11 |
        