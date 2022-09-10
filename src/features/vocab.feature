Feature: Vocabulary and Parts of Speech (POS)
    I want the model to have the necessary vocabulary, and appropriately handle the impact of words with different parts of speech on the task.

Scenario Outline: [MFT] When the input is the verbatim definition of an SDG, the prediction should be that SDG.
    Given I input "<text>"
    Then the model should be very confident that the input refers to SDG <n>

    Examples:
        | n  | text                                                                                     |    
        | 1  | End poverty in all its forms everywhere.                                                 |
        | 2  | End hunger, achieve food security and improved nutrition and promote sustainable agriculture. |
        | 3  | Ensure healthy lives and promote well-being for all at all ages.                              |
        | 4  | Ensure inclusive and equitable quality education and promote lifelong learning opportunities. |
        | 5  | Achieve gender equality and empower all women and girls.                                      |
        | 6  | Ensure availability and sustainable management of water and sanitation for all                |
        | 7  | Ensure access to affordable, reliable, sustainable and modern energy for all.                 |
        | 8  | Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all. |
        | 9  | Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation. |
        | 10 | Reduce inequality within and among countries.                                                 |
        | 11 | Make cities and human settlements inclusive, safe, resilient and sustainable                  |
        | 12 | Ensure sustainable consumption and production patterns.                                       |
        | 13 | Take urgent action to combat climate change and its impacts.                                  |
        | 14 | Conserve and sustainably use the oceans, seas and marine resources for sustainable development. |
        | 15 | Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss. |
        | 16 | Promote peaceful and inclusive societies for sustainable development, provide access to justice for all and build effective, accountable and inclusive institutions at all levels. |
        | 17 | Strengthen the means of implementation and revitalize the global partnership for sustainable development. |

Scenario Outline: [MDT] When the input does not refer to an SDG, the prediction should not be an SDG.
    Given I input "<text>"
    Then the model should be somewhat confident that the input does not refer to any SDG.

    Examples:
        | n  | text                                                                                     |
        | 1  | I'm poor right now.                                                                      |
        | 1  | Oh, poor little thing.                                                                   |
        | 2  | I’m hungry, let’s go to a restaurant.                                                    |
        | 3  | I’m sick, I need to go to the doctor.                                                    |
        | 4  | I’m going to school.                                                                     |
        | 6  | I need to drink water.                                                                   |
        | 6  | I need to take a shower.                                                                 |
        | 7  | I need to turn on the lights.                                                            |
        | 8  | I need to get a job.                                                                     |
        | 9  | I need to build a house.                                                                 |
        | 10 | I need to get a job.                                                                     |
        | 11 | I need to go to the city.                                                                |
        | 12 | I need to buy a new car.                                                                 |
        | 13 | I need to turn on the air conditioner.                                                   |
        | 14 | I need to go to the beach.                                                               |
        | 15 | I need to go to the forest.                                                              |
        | 16 | I am at peace.                                                                           |
        | 17 | Let's do a partnership to sell petrol                                                    |


# Scenario Outline: [MFT] When the input refers to a SDG with its number, the prediction should be that SDG.

