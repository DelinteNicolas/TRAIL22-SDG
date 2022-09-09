Feature: Vocabulary and Parts of Speech (POS)
    I want the model to have the necessary vocabulary, and appropriately handle the impact of words with different parts of speech on the task.

Scenario Outline: [MFT] When the input is the verbatim definition of an SDG, the prediction should be that SDG.
    Given I input "<text>"
    And the input is the verbatim definition of "<sdg>"
    Then the model should be very confident that the label is "<sdg>"

    Examples:
        | text                                                                                          | sdg                                       |
        | End poverty in all its forms everywhere.                                                      | SDG1: No Poverty                          |
        | End hunger, achieve food security and improved nutrition and promote sustainable agriculture. | SDG2: Zero Hunger                         |
        | Ensure healthy lives and promote well-being for all at all ages.                              | SDG3: Good Health and Well-being          |
        | Ensure inclusive and equitable quality education and promote lifelong learning opportunities. | SDG4: Quality Education                   |
        | Achieve gender equality and empower all women and girls.                                      | SDG5: Gender Equality                     |
        | Ensure availability and sustainable management of water and sanitation for all                | SDG6: Clean Water and Sanitation          |
        | Ensure access to affordable, reliable, sustainable and modern energy for all.                 | SDG7: Affordable and Clean Energy         |
        | Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all. | SDG8: Decent Work and Economic Growth |
        | Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation. | SDG9: Industry, Innovation and Infrastructure |
        | Reduce inequality within and among countries.                                                 | SDG10: Reduced Inequalities               |
        | Make cities and human settlements inclusive, safe, resilient and sustainable                  | SDG11: Sustainable Cities and Communities |
        | Ensure sustainable consumption and production patterns.                                       | SDG12: Responsible Consumption and Production |
        | Take urgent action to combat climate change and its impacts.                                  | SDG13: Climate Action                     |
        | Conserve and sustainably use the oceans, seas and marine resources for sustainable development. | SDG14: Life Below Water                   |
        | Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss. | SDG15: Life on Land |
        | Promote peaceful and inclusive societies for sustainable development, provide access to justice for all and build effective, accountable and inclusive institutions at all levels. | SDG16: Peace, Justice and Strong Institutions |
        | Strengthen the means of implementation and revitalize the global partnership for sustainable development. | SDG17: Partnerships |
