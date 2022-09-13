from behave import given, when, then


@given(u'I input "{text}"')
def step_impl(context, text: str):
    context.initial_text = text
    context.initial_sdgs = context.classifier.classify(text).assigned_sdgs()

@when(u'I wrote "{final_word}" instead of "{initial_word}"')
def step_impl(context, initial_word: str, final_word: str):
    context.final_text = context.initial_text.replace(initial_word, final_word)
    context.final_sdgs = context.classifier.classify(context.final_text).assigned_sdgs()

@when(u'I {action} as "{text}"')
def step_impl(context, action: str, text: str):
    context.final_text = text
    context.final_sdgs = context.classifier.classify(context.final_text).assigned_sdgs()
    
@then(u'SDG {n:d} should be the only assigned SDG')
def step_impl(context, n: int):
    print(f"[Initial] Text: {context.initial_text} => SDGs: {context.initial_sdgs}")
    assert context.initial_sdgs == [n]

@then(u'no SDGs should be assigned')
def step_impl(context):
    print(f"[Initial] Text: {context.initial_text} => SDGs: {context.initial_sdgs}")
    assert context.initial_sdgs == []

@then(u'the assigned SDGs should not change')
def step_impl(context):
    print(f"[Initial] Text: {context.initial_text} => SDGs: {context.initial_sdgs}")
    print(f"[Final] Text: {context.final_text} => SDGs: {context.final_sdgs}")
    assert context.initial_sdgs == context.final_sdgs

@then(u'SDG {n:d} should be part of the initial SDGs assigned')
def step_impl(context, n: int):
    print(f"[Initial] Text: {context.initial_text} => SDGs: {context.initial_sdgs}")
    assert n in context.initial_sdgs

@then(u'the number of initial SDGs assigned should be {n:d}')
def step_impl(context, n: int):
    print(f"[Initial] Text: {context.initial_text} => SDGs: {context.initial_sdgs}")
    assert len(context.initial_sdgs) == n

@then(u'SDG {n:d} should not be part of the final SDGs assigned')
def step_impl(context, n: int):
    print(f"[Final] Text: {context.final_text} => SDGs: {context.final_sdgs}")
    assert n not in context.final_sdgs