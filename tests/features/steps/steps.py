from behave import given, when, then, step
from utils import switch_gender, almost_equal, gender_neutral


@given(u'I input "{text}"')
def step_impl(context, text):
    context.pre_text = text
    context.pre_output = context.classifier.classify(text)


@when(u'I remove all gendered words')
def step_impl(context):
    context.post_text = context.pre_text
    for word in ["women", "Women", "men", "Men"]:
        context.post_text = context.post_text.replace(word, "")
    context.post_output = context.classifier.classify(context.post_text)


@then(u'SDG {n:d} should not be in the assigned SDGs anymore')
def step_impl(context, n: int):
    print(context.pre_output.assigned_sdgs(), context.post_output.assigned_sdgs())
    assert context.post_output.assigned_sdgs() == [i for i in context.pre_output.assigned_sdgs() if i not in [n]]

@then(u'SDG {n:d} should be the only assigned SDG')
def step_impl(context, n: int):
    print(context.pre_output.assigned_sdgs())
    assert context.pre_output.assigned_sdgs() == [n]

@then(u'no SDGs should be assigned')
def step_impl(context):
    print(context.pre_output.assigned_sdgs())
    assert context.pre_output.assigned_sdgs() == []
