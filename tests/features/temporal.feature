Feature: Temporal
    I want the model to understand the order of events

Scenario Outline: [MFT] When the goal changes over time, the present should prevail.
    Given I input "We used to aim to <past_text> but now we aim to <present_text>"
    Then SDG <n> should be part of the initial SDGs assigned
    And the number of initial SDGs assigned should be 1

    Examples:
        | past_text | present_text | n |
        | End poverty in all its forms everywhere | End hunger, achieve food security and improved nutrition and promote sustainable agriculture. | 2 |
        | End hunger, achieve food security and improved nutrition and promote sustainable agriculture | End poverty in all its forms everywhere. | 1 |
        | End poverty in all its forms everywhere | Ensure healthy lives and promote well-being for all at all ages. | 3 |
        | Ensure healthy lives and promote well-being for all at all ages | End poverty in all its forms everywhere. | 1 |
        | Ensure inclusive and equitable quality education and promote lifelong learning opportunities | End poverty in all its forms everywhere. | 1 |
        | Achieve gender equality and empower all women and girls                                      | Ensure availability and sustainable management of water and sanitation for all | 6 |
        | Ensure availability and sustainable management of water and sanitation for all                | Ensure access to affordable, reliable, sustainable and modern energy for all.                 | 7 |
        | Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all | Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation. | 9 |
        | Reduce inequality within and among countries                                                 | Make cities and human settlements inclusive, safe, resilient and sustainable                  |  11 | 