Feature: Named Entity Recognition
    I want the model to be robust to named entity

Scenario Outline: [INV] Switching locations should not change predictions.
    Given I input "<text>"
    When I wrote "<location2>" instead of "<location1>"
    Then the assigned SDGs should not change

    Examples:
        | n | text | location1 | location2 |
        | 1  | UNICEF aims, among others things, to eradicate extreme poverty in Africa. | Africa | Asia |
        | 2  | MacDonald wants to reduce food waste in Europe. | Europe | America |
        | 3  | Volkswagen wants to halve the number of deaths and injuries from road traffic accidents in Europe. | Europe | America |
        | 4  | School4All build schools in Benin. | Benin | Belgium |
        | 5  | NoGap want to reduce salary inequality between gender in France. | France | Germany |
        | 6  | TeamSeas wants to reduce water pollution in the Indian Ocean. | Indian Ocean | Pacific Ocean |
        | 7  | Total will switch to renewable energy in the North Sea. | North Sea | Atlantic Ocean |
        | 8  | The World Tourism Organization promotes sustainable tourism in the Caribbean Sea. | Caribbean Sea | Pacific Ocean |
        | 9  | UNICEF seek to incorporate inclusive and sustainable industrial development, as well as resilient infrastructure and innovation in China. | China | India |
        | 10 | NoGap aims to reduce inequality in South Africa | South Africa | South America |
        | 11 | Another interesting aspect of the city of Copenhagen is that two thirds of its hotels are eco-certified, which means that they meet the highest standards for sustainable energy, food and design. | Copenhagen | Paris |
        | 12 | The UN commit to making fundamental changes in the way that our societies produce and consume goods and services in Europe. | Europe | America |
        | 13 | The United States expresses its commitment to take urgent action to combat climate change in California. | California | New York |
        | 14 | TeamSeas is a global campaign to raise $30M to remove 30M pounds of plastic and trash from the Indian Ocean. | Indian Ocean | Pacific Ocean |
        | 15 | The Sustainable Development Goal 15 of the UN for Sustainable Development is devoted to “protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss in the Amazon Rainforest”. | Amazon Rainforest | Congo Rainforest |
        | 16 | Amnesty International will reduce corruption in Mexico. | Mexico | Brazil |
        | 17 | Amnesty International aims at strengthening and maintaining the capabilities of states and societies to design and implement strategies that minimize the negative impacts of current social, economic and environmental crises and emerging challenges in Scandinavia. | Scandinavia | Europe |

Scenario Outline: [INV] Switching organisations should not change predictions.
    Given I input "<text>"
    When I wrote "<organisation2>" instead of "<organisation1>"
    Then the assigned SDGs should not change

    Examples:
        | n  | text | organisation1 | organisation2 |
        | 1  | UNICEF aims, among others things, to eradicate extreme poverty. | UNICEF | UNHCR |
        | 2  | MacDonald wants to reduce food waste. | MacDonald | Nestlé |
        | 3  | Volkswagen wants to halve the number of deaths and injuries from road traffic accidents in Europe. | Volkswagen | Toyota |
        | 4  | School4All build schools for all. | School4All | UNICEF |
        | 5  | NoGap want to reduce salary inequality between gender. | NoGap | UNICEF |
        | 6  | TeamSeas wants to reduce water pollution. | TeamSeas | Mossy Earth |
        | 7  | Total will switch to renewable energy. | Total | Shell |
        | 8  | The World Tourism Organization promotes sustainable tourism. | The World Tourism Organization | Ryanair |
        | 9  | UNICEF seek to incorporate inclusive and sustainable industrial development, as well as resilient infrastructure and innovation.  |  UNICEF |  UNHCR |
        | 10 | NoGap aims to reduce inequality. | NoGap | UNICEF |
        | 11 | Another interesting aspect of Airport Hotel is that two thirds of its hotels are eco-certified, which means that they meet the highest standards for sustainable energy, food and design. | Airport Hotel | Ryanair |
        | 12 | The UN commit to making fundamental changes in the way that our societies produce and consume goods and services. |  UN |  UNICEF |
        | 13 | The European Union expresses its commitment to take urgent action to combat climate change. | European Union | United States |
        | 14 | TeamSeas is a global campaign to raise $30M to remove 30M pounds of plastic and trash from our ocean, rivers and beaches. | TeamSeas | Mossy Earth |
        | 15 | The Sustainable Development Goal 15 of the UN for Sustainable Development is devoted to “protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss”. | UN |  UNICEF |
        | 16 | Amnesty International will reduce corruption. | Amnesty International | Greenpeace |
        | 17 | Amnesty International aims at strengthening and maintaining the capabilities of states and societies to design and implement strategies that minimize the negative impacts of current social, economic and environmental crises and emerging challenges. | Amnesty International | Greenpeace |
        