Feature: Robustness
    I want the model to understand a text correctly, even if there are typos, irrelevant changes, etc.

Scenario Outline: [INV] Making a typo should not change the prediction
    Given I input "<text>"
    When I wrote "<misspelled>" instead of "<wellspelled>"
    Then the assigned SDGs should not change

    Examples:
    | n  | text | wellspelled | misspelled |
    | 1  | Its seven associated targets aims, among others, to eradicate extreme poverty. | poverty | povety |
    | 2  | We will reduce food waste. | food | fod |
    | 3  | We aim to halve the number of deaths and injuries from road traffic accidents. | deaths | deats |
    | 4  | We will build schools for all. | schools | scools |
    | 5  | This should reduce salary inequality between gender. | gender | geneder |
    | 6  | We will reduce water pollution. | water | watter |
    | 7  | We will switch to renewable energy. | energy | enery |
    | 8  | The World Tourism Organization promotes sustainable tourism. | tourism | toerism |
    | 9  | We seek to incorporate inclusive and sustainable industrial development, as well as resilient infrastructure and innovation.  | innovation | inovation |
    | 10 | We aim to reduce inequality. | inequality | inequlity |
    | 11 | Another interesting aspect of the city of Copenhagen is that two thirds of its hotels are eco-certified, which means that they meet the highest standards for sustainable energy, food and design. | city | citty |
    | 12 | We (Countries) commit to making fundamental changes in the way that our societies produce and consume goods and services. | consume | comsume |
    | 13 | We aim to be carbon neutral by 2050. | carbon | carbin |
    | 14 | TeamSeas is a global campaign to raise $30M to remove 30M pounds of plastic and trash from our ocean, rivers and beaches. | sea | see |
    | 15 | The Sustainable Development Goal 15 of the 2030 Agenda for Sustainable Development is devoted to “protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss”. | forest | forrest |
    | 16 | We will reduce corruption. | corruption | coruption |
    | 17 | Capacity building activities are also aimed at strengthening and maintaining the capabilities of states and societies to design and implement strategies that minimize the negative impacts of current social, economic and environmental crises and emerging challenges. | states | stetes |

Scenario Outline: [INV] Paraphrasing should not change the prediction
    Given I input "<text>"
    When I paraphrase as "<paraphrase>"
    Then the assigned SDGs should not change

    Examples:
    | n  | text | paraphrase |
    | 1  | Its seven associated targets aims, among others, to eradicate extreme poverty. | Its seven related goals aim to alleviate severe poverty, among other things. |
    | 2  | We will reduce food waste. |  We'll cut down on food waste. |
    | 3  | We aim to halve the number of deaths and injuries from road traffic accidents. |  The number of fatalities and injuries resulting from traffic accidents must be cut in half. |
    | 4  | We'll construct schools for everyone. | We will build educational facilities for all students. |
    | 5  | This should reduce salary inequality between gender. | This should lessen the pay gap between men and women. |
    | 6  | We will reduce water pollution. | We'll clean up the water. |
    | 7  | We will switch to renewable energy. | We'll use renewable energy instead. |
    | 8  | The World Tourism Organization promotes sustainable tourism. | The World Tourism Organization encourages environmentally friendly travel. |
    | 9  | We seek to incorporate inclusive and sustainable industrial development, as well as resilient infrastructure and innovation.  | We want to include robust infrastructure, innovation, and inclusive and sustainable industrial growth. |
    | 10 | We aim to reduce inequality. | We want to reduce inequality. |
    | 11 | Another interesting aspect of the city of Copenhagen is that two thirds of its hotels are eco-certified, which means that they meet the highest standards for sustainable energy, food and design. | Copenhagen's two-thirds eco-certified hotels, which adhere to the highest standards for sustainable energy, food, and design, are another intriguing feature of the capital.
    | 12 | We (Countries) commit to making fundamental changes in the way that our societies produce and consume goods and services. | We (Countries) pledge to modify society's production and use of commodities and services fundamentally. |
    | 13 | The European Union expresses its commitment to take urgent action to combat climate change. | The European Union declares its will to act quickly to tackle climate change. |
    | 14 | TeamSeas is a global campaign to raise $30M to remove 30M pounds of plastic and trash from our ocean, rivers and beaches. | The goal of the $30 million TeamSeas effort is to collect 30 million pounds of plastic and other rubbish from our oceans, rivers, and beaches. |
    | 15 | The Sustainable Development Goal 15 of the 2030 Agenda for Sustainable Development is devoted to “protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss”. | In order to "protect, restore, and promote sustainable use of terrestrial ecosystems, sustainably manage forests, battle desertification, and halt and reverse land degradation and prevent biodiversity loss," Sustainable Development Goal 15 of the 2030 Agenda for Sustainable Development was established. |
    | 16 | We will reduce corruption. |  We'll fight against corruption. |
    | 17 | Capacity building activities are also aimed at strengthening and maintaining the capabilities of states and societies to design and implement strategies that minimize the negative impacts of current social, economic and environmental crises and emerging challenges. | Activities to create capacity also strive to preserve and increase societies' and states' ability to develop and put into practise plans that lessen the effects of ongoing social, economic, and environmental crises and new challenges. |
    # | I want to reduce poverty. | I desire to lessen poverty. |
    # | We will switch to renewable energy. | We'll use green energy instead. |
    # | We aim to reduce inequality. | Our goal is to lessen inequity. |
    # | We aim to be carbon neutral by 2050. | By 2050, we want to be carbon neutral. |
    # | We will reduce food waste. | We'll cut down on food waste. |
    # | We will reduce water pollution. | We'll lessen the water contamination. |
    # | We will reduce air pollution. | Air pollution will be decreased. |
    # | We will reduce plastic waste. | We'll cut down on plastic trash. |
    # | We will reduce deforestation. | We'll stop further deforestation. |
    # | We will reduce biodiversity loss. | We will stop the extinction of endangered species. |

