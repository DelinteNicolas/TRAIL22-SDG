Feature: Fairness
    I want the model to be fair

Scenario Outline: [DIR] With a sentence about SDG 5 and another SDG, when I remove all gendered words, SDG 5 is not present anymore
    Given I input "<text>"
    When I remove all gendered words
    Then SDG 5 should not be in the assigned SDGs anymore

    Examples:
        | text |
        | Women for Nature is the collaborative voices of Canadian women with vision – women of influence who chose to demonstrate their passion for nature and pass their values on to others to drive change. |
        | Women make up close to half the world’s population, and although they are often disproportionately impacted by climate change, their voices are not always heard due to lack of inclusion and representation at the decision-making level. 
        | Now more than ever, enhancing women’s participation and leadership in the conversation around climate action will be critical to securing a healthy, prosperous and sustainable future for us all. |