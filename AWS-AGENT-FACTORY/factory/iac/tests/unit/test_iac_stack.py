import aws_cdk as core
import aws_cdk.assertions as assertions
from iac.iac_stack import IacStack

def test_bedrock_agent_created():
    app = core.App()
    stack = IacStack(app, "iac")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::Bedrock::Agent", {
        "AgentName": "sre-assistant",
        "FoundationModel": "anthropic.claude-3-sonnet-20240229-v1:0"
    })

def test_iam_role_created():
    app = core.App()
    stack = IacStack(app, "iac")
    template = assertions.Template.from_stack(stack)

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
    app = core.App()
    stack = IacStack(app, "iac")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::Lambda::Function", {
        "Runtime": "go1.x",
        "Handler": "main"
    })