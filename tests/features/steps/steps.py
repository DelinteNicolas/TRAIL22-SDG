from behave import given, when, then, step
from utils import switch_gender, almost_equal, gender_neutral


@given(u'I input "{text}"')
def step_impl(context, text: str):
    context.pre_text = text
    context.pre_output = context.classifier.classify(text)

@when(u'I wrote "{changed_word}" instead of "{initial_word}"')
def step_impl(context, changed_word: str, initial_word: str):
    context.post_text = context.pre_text.replace(initial_word, changed_word)
    context.post_output = context.classifier.classify(context.post_text)

@when(u'I {action} as "{paraphrase}"')
def step_impl(context, action: str, paraphrase: str):
    context.post_text = paraphrase
    context.post_output = context.classifier.classify(context.post_text)
    
@then(u'SDG {n:d} should be the only assigned SDG')
def step_impl(context, n: int):
    print(context.pre_output.assigned_sdgs())
    assert context.pre_output.assigned_sdgs() == [n]

@then(u'no SDGs should be assigned')
def step_impl(context):
    print(context.pre_output.assigned_sdgs())
    assert context.pre_output.assigned_sdgs() == []

@then(u'the assigned SDGs should not change')
def step_impl(context):
    print(context.pre_output.assigned_sdgs(), context.post_output.assigned_sdgs())
    assert context.pre_output.assigned_sdgs() == context.post_output.assigned_sdgs()

@then(u'SDG {n:d} should be part of the initial SDGs assigned')
def step_impl(context, n: int):
    assert n in context.pre_output.assigned_sdgs()

@then(u'the number of initial SDGs assigned should be {n:d}')
def step_impl(context, n: int):
    assert len(context.pre_output.assigned_sdgs()) == n

@then(u'SDG {n:d} should not be part of the final SDGs assigned')
def step_impl(context, n: int):
    assert n not in context.post_output.assigned_sdgs()