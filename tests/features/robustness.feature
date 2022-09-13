Feature: Robustness
    I want the model to be robust to typos, irrelevant changes, etc

Scenario Outline: [INV] Making a typo should not change the prediction
    Given I input "<text>"
    When I wrote "<misspelled>" instead of "<wellspelled>"
    Then the assigned SDGs should not change

    Examples:
    | text | misspelled | wellspelled |
    | I want to reduce poverty | povert | poverty |
    | We will switch to renewable energy | renwable | renewable |
    | We aim to reduce inequality | inequalty | inequality |
    | We aim to be carbon neutral by 2050 | carbon netral | carbon neutral |
    | We will reduce food waste | food wast | food waste |
    | We will reduce water pollution | water polution | water pollution |
    | We will reduce air pollution | air polution | air pollution |
    | We will reduce plastic waste | plastic wast | plastic waste |
    | We will reduce deforestation | deforrestation | deforestation |
    | We will reduce biodiversity loss | biodiversety loss | biodiversity loss |

Scenario Outline: [INV] Paraphrasing should not change the prediction
    Given I input "<text>"
    When I paraphrase as "<paraphrase>"
    Then the assigned SDGs should not change

    Examples:
    | text | paraphrase |
    | I want to reduce poverty. | I desire to lessen poverty. |
    | We will switch to renewable energy. | We'll use green energy instead. |
    | We aim to reduce inequality. | Our goal is to lessen inequity. |
    | We aim to be carbon neutral by 2050. | By 2050, we want to be carbon neutral. |
    | We will reduce food waste. | We'll cut down on food waste. |
    | We will reduce water pollution. | We'll lessen the water contamination. |
    | We will reduce air pollution. | Air pollution will be decreased. |
    | We will reduce plastic waste. | We'll cut down on plastic trash. |
    | We will reduce deforestation. | We'll stop further deforestation. |
    | We will reduce biodiversity loss. | We will stop the extinction of endangered species. |

