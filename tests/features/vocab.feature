Feature: Vocabulary and Parts of Speech (POS)
    I want the model to appropriately handle the impact of words with different parts of speech on the task.

Scenario Outline: [MFT] When the input clearly refers to an SDG, the prediction should be that SDG.
    Given I input "<text>"
    Then SDG <n> should be part of the initial SDGs assigned
    And the number of initial SDGs assigned should be 1

    Examples: Verbatim definitions of SDGs
        | n  | text |
        | 1  | I want to reduce poverty. |
        | 2  | We will reduce food waste. |
        | 3  | We will reduce air pollution. |
        | 4  | We will build schools for all. |
        | 5  | This should reduce salary inequality between gender. |
        | 6  | We will reduce water pollution. | 
        | 7  | We will switch to renewable energy. |
        | 8  | Child labour must be banned worldwide. |
        | 9  | Public transport is now free in Luxembourg.  |
        | 10 | We aim to reduce inequality. |
        | 11 | Another interesting aspect of the city of Copenhagen is that two thirds of its hotels are eco-certified, which means that they meet the highest standards for sustainable energy, food and design. |
        | 12 | We will reduce plastic waste. |
        | 13 | We aim to be carbon neutral by 2050. |
        | 14 | TeamSeas is a global campaign to raise $30M to remove 30M pounds of plastic and trash from our ocean, rivers and beaches.
        | 15 | We will reduce deforestation. |
        | 15 | We will reduce biodiversity loss. |
        # | 16 | We will reduce corruption. |
        # | 17 | We will support the UN's 17 SDGs. |

Scenario Outline: [MFT] When an input is purely informative, the prediction should not be any SDG.
    Given I input "<text>"
    Then no SDGs should be assigned

    Examples:
        | text                                          |
        | Poverty is the state of having few material possessions or little income. | 
        | I am so hungry right now.     |
        | Namur is a city in Belgium. |
        | The meaning of health has evolved over time. |
        | I walked in the forest last night. |

