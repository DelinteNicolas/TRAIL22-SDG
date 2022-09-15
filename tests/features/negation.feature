Feature: Negation
    I want the model to understand the impact of negation correctly.

Scenario Outline: [DIR] When I negate a sentence, the model should not assign a SDG
    Given I input "<text>"
    When I negate as "<negation>"
    Then SDG <n> should be part of the initial SDGs assigned
    And SDG <n> should not be part of the final SDGs assigned

    Examples:
        | n  | text | negation |
        | 1  | Its seven associated targets aims, among others, to eradicate extreme poverty. | Its seven associated targets does not aim, among others, to eradicate extreme poverty. |
        | 2  | We will reduce food waste. | We will not reduce food waste. |
        | 3  | We aim to halve the number of deaths and injuries from road traffic accidents. | We do not aim to halve the number of deaths and injuries from road traffic accidents. |
        | 4  | We will build schools for all. | We will not build schools for all. |
        | 5  | This should reduce salary inequality between gender. | This should not reduce salary inequality between gender |
        | 6  | We will reduce water pollution. | We will not reduce water pollution. |
        | 7  | We will switch to renewable energy. | We will not switch to renewable energy. |
        | 8  | The World Tourism Organization promotes sustainable tourism. | The World Tourism Organization does not promote sustainable tourism. |
        | 9  | We seek to incorporate inclusive and sustainable industrial development, as well as resilient infrastructure and innovation.  | We seek to not incorporate inclusive and sustainable industrial development, as well as resilient infrastructure and innovation. |
        | 10 | We aim to reduce inequality. | We aim to not reduce inequality. |
        | 11 | Another interesting aspect of the city of Copenhagen is that two thirds of its hotels are eco-certified, which means that they meet the highest standards for sustainable energy, food and design. | Another interesting aspect of the city of Copenhagen is that two thirds of its hotels are not eco-certified, which means that they do not meet the highest standards for sustainable energy, food and design. |
        | 12 | We (Countries) commit to making fundamental changes in the way that our societies produce and consume goods and services. | We (Countries) commit to not making fundamental changes in the way that our societies produce and consume goods and services. |
        | 13 | The European Union expresses its commitment to take urgent action to combat climate change. | The European Union expresses its commitment to not take urgent action to combat climate change. |
        | 14 | TeamSeas is a global campaign to raise $30M to remove 30M pounds of plastic and trash from our ocean, rivers and beaches. | TeamSeas is not a global campaign to raise $30M to remove 30M pounds of plastic and trash from our ocean, rivers and beaches. |
        | 15 | The Sustainable Development Goal 15 of the 2030 Agenda for Sustainable Development is devoted to “protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss”. | The Sustainable Development Goal 15 of the 2030 Agenda for Sustainable Development is not devoted to “protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss”. |
        | 16 | We will reduce corruption. | We will not reduce corruption. |
        | 17 | Capacity building activities are also aimed at strengthening and maintaining the capabilities of states and societies to design and implement strategies that minimize the negative impacts of current social, economic and environmental crises and emerging challenges. | Capacity building activities are also aimed at not strengthening and maintaining the capabilities of states and societies to design and implement strategies that minimize the negative impacts of current social, economic and environmental crises and emerging challenges. |
        # | Our goal is to create inclusive, secure, resilient, and sustainable cities | Our goal is not to create inclusive, secure, resilient, and sustainable cities | 11 |
        