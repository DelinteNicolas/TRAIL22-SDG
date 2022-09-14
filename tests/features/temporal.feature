Feature: Temporal
    I want the model to understand the order of events

Scenario Outline: [MFT] When the goal changes over time, the present should prevail.
    Given I input "We used to aim to <past_text> but now we aim to <present_text>"
    Then SDG <n> should be part of the initial SDGs assigned
    And the number of initial SDGs assigned should be 1

    Examples:
        | past_text | present_text | n |
        | reduce food waste | eradicate extreme poverty | 1 |
        | eradicate extreme poverty | reduce food waste | 2 |
        | reduce water pollution | reduce air pollution | 3 |
        | reduce salary inequality between gender | build schools for all | 4 |
        | build schools for all | reduce salary inequality between gender | 5 |
        | reduce air pollution | reduce water pollution | 6 |
        | be carbon neutral by 2050 | switch to renewable energy | 7 |
        | promotes sustainable cities | promotes sustainable tourism | 8 |
        | consume sustainably | seek sustainable industrial development | 9 |
        | halt biodiversity loss | reduce inequality | 10 |
        | promotes sustainable tourism | promotes sustainable cities | 11 |
        | seek sustainable industrial development | consume sustainably | 12 |
        | switch to renewable energy | be carbon neutral by 2050 | 13 |
        | be carbon neutral by 2050 | switch to renewable energy | 14 |
        | reduce inequality | halt biodiversity loss | 15 |
        | increase cooperation | reduce corruption | 16 |
        | reduce corruption | increase cooperation | 17 |
        
        
