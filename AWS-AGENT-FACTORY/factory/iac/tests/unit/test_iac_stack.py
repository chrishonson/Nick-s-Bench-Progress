
import aws_cdk as core
import aws_cdk.assertions as assertions
from iac.iac_stack import IacStack

# These are AWS CDK unit tests that verify the CloudFormation template synthesized
# from the `IacStack`. They run locally without deploying actual AWS resources.
#
# To run these tests:
# 1. Ensure Docker is running if you are using GoFunction or other constructs that require local bundling.
#    Alternatively, you can synthesize the CDK app with `cdk synth --no-staging` to skip bundling.
# 2. Navigate to the `factory/iac` directory in your terminal.
# 3. Execute the tests using pytest: `python -m pytest tests/unit/test_iac_stack.py -v`

def test_bedrock_agent_created():
    """
    Tests if an AWS Bedrock Agent resource is created with the expected properties.
    This test synthesizes the CDK stack into a CloudFormation template and then
    asserts that a resource of type `AWS::Bedrock::Agent` exists with the specified
    `AgentName` and `FoundationModel`.
    """
    app = core.App(context={"test_mode": "true"})
    # Create an instance of the IacStack, which defines your AWS infrastructure.
    stack = IacStack(app, "iac")
    # Synthesize the stack into a CloudFormation template for testing.
    template = assertions.Template.from_stack(stack)

    # Assert that the template contains a resource with these properties.
    template.has_resource_properties("AWS::Bedrock::Agent", {
        "AgentName": "sre-assistant",
        "FoundationModel": "anthropic.claude-3-sonnet-20240229-v1:0"
    })

def test_iam_role_created():
    """
    Tests if an AWS IAM Role resource is created with the correct assume role policy.
    This ensures that the Bedrock service has the necessary permissions to assume
    this role, which is crucial for the Bedrock Agent's operation.
    """
    app = core.App(context={"test_mode": "true"})
    stack = IacStack(app, "iac")
    template = assertions.Template.from_stack(stack)

    # Assert that an IAM Role exists with a policy allowing Bedrock to assume it.
    template.has_resource_properties("AWS::IAM::Role", {
        "AssumeRolePolicyDocument": {
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "bedrock.amazonaws.com"
                    }
                }
            ]
        }
    })

def test_lambda_function_created():
    """
    Tests if an AWS Lambda Function resource is created.
    The `GoFunction` construct handles the runtime and handler details internally,
    so this test primarily checks for the existence of the Lambda function resource
    in the synthesized CloudFormation template.
    """
    app = core.App(context={"test_mode": "true"})
    stack = IacStack(app, "iac")
    template = assertions.Template.from_stack(stack)

    # Assert that a Lambda Function resource is present in the template.
    template.has_resource_properties("AWS::Lambda::Function", {
        # GoFunction handles runtime and handler internally
    })
