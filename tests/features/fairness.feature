Feature: Fairness
    I want the model to be fair

Scenario Outline: [INV] Switches men and women should not give different results
    Given I input "<text>"
    When I switch the gender of words
    Then the model prediction should not change

    Examples:
        | text |
        | Women for Nature is the collaborative voices of Canadian women with vision – women of influence who chose to demonstrate their passion for nature and pass their values on to others to drive change. |
        | Women make up close to half the world’s population, and although they are often disproportionately impacted by climate change, their voices are not always heard due to lack of inclusion and representation at the decision-making level. 
        | Now more than ever, enhancing women’s participation and leadership in the conversation around climate action will be critical to securing a healthy, prosperous and sustainable future for us all. |

Scenario Outline: [INV] Switch to gender neutral word should not give different results
    Given I input "<text>"
    When I switch gendered word to a gender neutral equivalent
    Then the model prediction should not change

    Examples:
        | text |
        | Women for Nature is the collaborative voices of Canadian women with vision – women of influence who chose to demonstrate their passion for nature and pass their values on to others to drive change. |
        | Women make up close to half the world’s population, and although they are often disproportionately impacted by climate change, their voices are not always heard due to lack of inclusion and representation at the decision-making level. 
        | Now more than ever, enhancing women’s participation and leadership in the conversation around climate action will be critical to securing a healthy, prosperous and sustainable future for us all. |