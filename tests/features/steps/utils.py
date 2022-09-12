def switch_gender(text: str) -> str:
    """
    Switch the gender of all words in a string.
    """
    GENDER_MAP = {
      "boy": "girl", 
      "girl": "boy",
      "father": "mother", 
      "mother": "father",
      "husband": "wife", 
      "wife": "husband",
      "boyfriend": "girlfriend",
      "girlfriend": "boyfriend",
      "he": "she", 
      "she": "he",
      "his": "her",
      "her": "his",
      "male": "female",
      "female": "male",
      "man": "woman",
      "woman": "man",
      "mr": "ms",
      "mr": "ms",
      "sir": "madam",
      "madam": "sir",
      "son": "daughter",
      "daughter": "son",
      "uncle": "aunt",
      "aunt": "uncle",
      "men": "women",
      "women": "men",
      "men's": "women's",
      "women's": "men's",
    }
    text = text.lower()
    for key in GENDER_MAP.keys():
        text = text.replace(f' {key} ', f'@#~{key}~#@')
    for key, value in GENDER_MAP.items():
        text = text.replace(f'@#~{key}~#@', f' {value} ')
    return text

def gender_neutral(text: str) -> str:
    """
    Switch gendered words to a gender neutral equivalent.
    """
    GENDER_MAP = {
      "boy": "child", 
      "girl": "child",
      "father": "parent", 
      "mother": "parent",
      "husband": "spouse", 
      "wife": "spouse",
      "boyfriend": "spouse",
      "girlfriend": "spouse",
      "he": "they", 
      "she": "they",
      "his": "their",
      "her": "their",
      "male": "",
      "female": "",
      "man": "person",
      "woman": "person",
      "men": "people",
      "women": "people",
      "mr": "",
      "mr": "",
      "sir": "",
      "madam": "",
      "son": "child",
      "daughter": "child",
      "men's": "people's",
      "women's": "people's",
    }
    text = text.lower()
    for key in GENDER_MAP.keys():
        text = text.replace(f' {key} ', f'@#~{key}~#@')
    for key, value in GENDER_MAP.items():
        text = text.replace(f'@#~{key}~#@', f' {value} ')
    return text

def almost_equal(a, b, tol=1e-6):
    return abs(a-b) < tol