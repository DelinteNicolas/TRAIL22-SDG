from behave import given, when, then, step


@given('I input "{text}"')
def step_impl(context, text):
    context.output = context.classifier(text)
    print(context.output)

@given('the input is the verbatim definition of "{sdg}"')
def step_impl(context, sdg):
    context.expected_label = sdg

@then('the model should be very confident that the label is "{sdg}"')
def step_impl(context, sdg):
    
    assert context.output[0]['label'] == sdg
    assert context.output[0]['score'] > 0.9

