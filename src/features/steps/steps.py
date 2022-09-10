from behave import given, when, then, step


@given('I input "{text}"')
def step_impl(context, text):
    context.output = context.classifier.classify(text)
    print(context.output)

@then('the model should be very confident that the input refers to SDG {n:d}')
def step_impl(context, n: int):
    assert context.output.label == n
    assert context.output.class_predictions[n] >= 0.9

@then(u'the model should be somewhat confident that the input does not refer to any SDG.')
def step_impl(context):
    assert context.output.confidence < 0.5

