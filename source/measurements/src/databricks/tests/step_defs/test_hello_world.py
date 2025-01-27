import pytest
from pytest_bdd import scenarios, given, when, then

scenarios("../features/hello_world.feature")

@pytest.fixture
def context():
    return {}

@given("the system is running")
def system_running():
    # No specific setup needed for this basic example
    pass

@when('I print "Hello"')
def i_print_hello(context):
    context["output"] = "Hello"

@then('I should see the text "Hello"')
def i_should_see_the_text_hello(context):
    assert context["output"] == "Hello"

