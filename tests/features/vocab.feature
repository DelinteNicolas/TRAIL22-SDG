Feature: Vocabulary and Parts of Speech (POS)
    I want the model to understand the impact of words correctly.

Scenario Outline: [MFT] When the input refers to an SDG, the prediction should be that SDG.
    Given I input "<text>"
    Then SDG <n> should be part of the initial SDGs assigned
    And the number of initial SDGs assigned should be 1

    Examples:
        | n  | text |
        | 1  | Its seven associated targets aims, among others, to eradicate extreme poverty. |
        | 2  | We will reduce food waste. |
        | 3  | We aim to halve the number of deaths and injuries from road traffic accidents. |
        | 4  | We will build schools for all. |
        | 5  | This should reduce salary inequality between gender. |
        | 6  | We will reduce water pollution. | 
        | 7  | We will switch to renewable energy. |
        | 8  | The World Tourism Organization promotes sustainable tourism. |
        | 9  | We seek to incorporate inclusive and sustainable industrial development, as well as resilient infrastructure and innovation.  |
        | 10 | We aim to reduce inequality. |
        | 11 | Another interesting aspect of the city of Copenhagen is that two thirds of its hotels are eco-certified, which means that they meet the highest standards for sustainable energy, food and design. |
        | 12 | We (Countries) commit to making fundamental changes in the way that our societies produce and consume goods and services. |
        | 13 | The European Union expresses its commitment to take urgent action to combat climate change. |
        | 14 | TeamSeas is a global campaign to raise $30M to remove 30M pounds of plastic and trash from our ocean, rivers and beaches. |
        | 15 | The Sustainable Development Goal 15 of the 2030 Agenda for Sustainable Development is devoted to “protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss”. |
        | 16 | We will reduce corruption. |
        | 17 | Capacity building activities are also aimed at strengthening and maintaining the capabilities of states and societies to design and implement strategies that minimize the negative impacts of current social, economic and environmental crises and emerging challenges. |

Scenario Outline: [MFT] When the input does not refer to an SDG, the prediction should not be any SDG.
    Given I input "<text>"
    Then no SDGs should be assigned

    Examples:
        | n | text |
        | 1 | Poverty is the state of having few material possessions or little income. |
        | 2 | I am so hungry right now. |
        | 3 | Being healthy is all that matters. |
        | 4 | A school is an educational institution designed to provide learning spaces and learning environments for the teaching of students under the direction of teachers. |
        | 5 | Gender is the range of characteristics pertaining to femininity and masculinity and differentiating between them. |
        | 6 | The ancient Greeks believed that there were four elements that everything was made up of: earth, water, air, and fire. |
        | 7 | In physics, energy is the quantitative property that is transferred to a body or to a physical system, recognizable in the performance of work and in the form of heat and light. |
        | 8 | Tourism is travel for pleasure or business; also the theory and practice of touring, the business of attracting, accommodating, and entertaining tourists, and the business of operating tours. |
        | 9 | Innovation is the practical implementation of ideas that result in the introduction of new goods or services or improvement in offering goods or services. |
        | 10 | In economics, the Gini coefficient, also known as the Gini index or Gini ratio, is a measure of statistical dispersion intended to represent the income inequality or the wealth inequality within a nation or a social group. |
        | 11 | Namur is a city in Belgium. |
        | 12 | A consumer is a person or a group who intends to order, orders, or uses purchased goods, products, or services primarily for personal, social, family, household and similar needs, not directly related to entrepreneurial or business activities. |
        | 13 | Climate change denial, or global warming denial, is denial, dismissal, or unwarranted doubt that contradicts the scientific consensus on climate change, including the extent to which it is caused by humans, its effects on nature and human society, or the potential of adaptation to global warming by human actions. |
        | 14 | The Principality of Sealand is an unrecognized micronation that claims HM Fort Roughs (also known as Roughs Tower), an offshore platform in the North Sea approximately twelve kilometres off the coast of Suffolk, as its territory. |
        | 15 | The Ardennes, also known as the Ardennes Forest or Forest of Ardennes, is a region of extensive forests, rough terrain, rolling hills and ridges primarily in Belgium and Luxembourg, extending into Germany and France. |
        | 16 | Peace is a concept of societal friendship and harmony in the absence of hostility and violence. |
        | 17 | Cooperation is the process of groups of organisms working or acting together for common, mutual, or some underlying benefit, as opposed to working in competition for selfish benefit. |

