from behave import given, when, then, step
from utils import switch_gender, almost_equal, gender_neutral


@given('I input "{text}"')
def step_impl(context, text):
    context.pre_text = text
    context.pre_output = context.classifier.classify(text)

@when(u'I switch the gender of words')
def step_impl(context):
    context.post_text = switch_gender(context.pre_text)
    print(context.post_text)
    context.post_output = context.classifier.classify(context.post_text)

@when(u'I switch gendered word to a gender neutral equivalent')
def step_impl(context):
    context.post_text = gender_neutral(context.pre_text)
    print(context.post_text)
    context.post_output = context.classifier.classify(context.post_text)


@then(u'the model prediction should not change')
def step_impl(context):
    assert context.post_output.label == context.pre_output.label
    assert almost_equal(context.post_output.confidence, context.pre_output.confidence, tol=1e-2)


@then('the model should be very confident that the input refers to SDG {n:d}')
def step_impl(context, n: int):
    assert context.pre_output.label == n
    assert context.pre_output.class_predictions[n] >= 0.9

@then(u'the model should be very confident that the input does not refer to any SDG.')
def step_impl(context):
    assert context.pre_output.confidence < 0.1

