Feature: Named Entity Recognition
    I want the model to be robust to named entity

Scenario Outline: [INV] Switching locations should not change predictions.
    Given I input "<text>"
    When I wrote "<location2>" instead of "<location1>"
    Then the assigned SDGs should not change

    Examples:
        | text | location1 | location2 |
        | UNICEF is building new schools in Africa. | Africa | Asia |
        | Mossy Earth is planting trees in Iceland. | Iceland | Benin |
        | The Water Project is digging wells in the Sahara desert. | the Sahara | the Gobi |

Scenario Outline: [INV] Switching organisations should not change predictions.
    Given I input "<text>"
    When I wrote "<organisation2>" instead of "<organisation1>"
    Then the assigned SDGs should not change

    Examples:
        | text | organisation1 | organisation2 |
        | UNICEF is building new schools in Africa. | UNICEF | UNHCR |
        | Mossy Earth is planting trees in Iceland. | Mossy Earth | Greenpeace |
        | The Water Project is digging wells in the Sahara desert. | The Water Project | WaterAid |
        