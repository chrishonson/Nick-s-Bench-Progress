
import yaml
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_bedrock as bedrock,
    aws_lambda as _lambda,
)
from constructs import Construct

class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Read the agent specification from the YAML file
        with open("../../agents/sre-assistant/spec.yaml", 'r') as stream:
            try:
                agent_spec = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        # Create the IAM role for the Bedrock Agent
        agent_role = iam.Role(
            self, "BedrockAgentRole",
            assumed_by=iam.ServicePrincipal("bedrock.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"),
            ],
        )

        # Create the Lambda function for the Action Group
        action_group_lambda = _lambda.Function(
            self, "ActionGroupLambda",
            runtime=_lambda.Runtime.GO_1_X,
            handler="main",
            code=_lambda.Code.from_asset("../src/hello-world"),
        )

        # Create the Bedrock Agent Action Group
        action_group = bedrock.CfnAgent.AgentActionGroupProperty(
            action_group_name="HelloWorldActionGroup",
            action_group_executor=bedrock.CfnAgent.ActionGroupExecutorProperty(
                lambda_=action_group_lambda.function_arn
            ),
            action_group_state="ENABLED",
            description="A default hello world action group."
        )

        # Create the Bedrock Agent
        agent = bedrock.CfnAgent(
            self, "MyBedrockAgent",
            agent_name=agent_spec['metadata']['name'],
            foundation_model=agent_spec['spec']['foundationModelId'],
            agent_resource_role_arn=agent_role.role_arn,
            action_groups=[action_group],
        )
