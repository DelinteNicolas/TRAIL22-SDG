Feature: Temporal
    I want the model to understand the order of events correctly.

Scenario Outline: [DIR] Switching the order of events should change the prediction
    Given I input "We used to aim to <text1> but now we aim to <text2>"
    When I switch the temporality as "We used to aim to <text2> but now we aim to <text1>"
    Then the initial SDGs assigned should be different than the final SDGs assigned
    And the number of initial SDGs assigned should be 1
    And the number of final SDGs assigned should be 1
    
    Examples:
        | text1 | text2 | n1 | n2 |
        | reduce food waste | eradicate extreme poverty | 2 | 1 |
        | eradicate extreme poverty | reduce food waste | 1 | 2 |
        | reduce water pollution | halve the number of deaths on the roads | 6 | 3 |
        | reduce salary inequality between gender | build schools for all | 5 | 4 |
        | build schools for all | reduce salary inequality between gender | 4 | 5 |
        | halve the number of deaths on the roads | reduce water pollution | 3 | 6 |
        | to combat climate change | switch to renewable energy | 13 | 7 |
        | promotes sustainable cities | promotes sustainable tourism | 11 | 8 |
        | consume sustainably | seek sustainable industrial development | 12 | 9 |
        | halt biodiversity loss | reduce inequality | 15 | 10 |
        | promotes sustainable tourism | promotes sustainable cities | 8 | 11 |
        | seek sustainable industrial development | consume sustainably | 9 | 12 |
        | switch to renewable energy | to combat climate change | 7 | 13 |
        | to combat climate change | switch to renewable energy | 13 | 7 |
        | reduce inequality | halt biodiversity loss | 10 | 15 |
        | increase cooperation | reduce corruption | 16 | 17 |
        | reduce corruption | increase cooperation | 17 | 16 |
        
        
