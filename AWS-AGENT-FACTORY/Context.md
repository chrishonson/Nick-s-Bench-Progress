V2 Blueprint: The GitOps Agent Factory
This document outlines the technical plan for building a GitOps-driven factory that creates and manages Amazon Bedrock AI Agents within a monorepo structure.

1. Confirmed Architecture
Agent Type: Amazon Bedrock AI Agent.

Interaction Model: GitOps Workflow.

Codebase Structure: Monorepo.

2. The GitOps Workflow Explained
The entire lifecycle of an agent—from creation to updates—will be managed through Git commits.

Trigger: A developer defines a new agent by adding a new sub-directory inside the /agents directory in our monorepo. This directory will contain a spec.yaml file.

Action: The developer commits this new file and pushes it to the main branch of the Git repository.

Pipeline: This push automatically triggers a CI/CD pipeline (e.g., AWS CodePipeline or GitHub Actions).

Factory Execution: The pipeline runs the "Factory" logic. The factory is a script that reads the spec.yaml file.

Deployment: The factory synthesizes and deploys the necessary AWS resources (the Bedrock Agent, its Action Groups, Lambda functions, and IAM roles) using the AWS Cloud Development Kit (CDK).

Here is a high-level visual of the flow:

+-----------+     +------------------+     +-----------------+     +---------------------+
| Developer | --> | git push         | --> | CI/CD Pipeline  | --> | "The Factory"       |
| (creates  |     | (to main branch) |     | (CodePipeline/  |     | (CDK script)        |
| spec.yaml)|     +------------------+     |  GitHub Actions)|     +----------+----------+
+-----------+                              +-----------------+                |
                                                                              | deploys
                                                                              v
                                                                +-------------------------+
                                                                | AWS Resources           |
                                                                | - Bedrock Agent         |
                                                                | - Lambda (Action Group) |
                                                                | - IAM Roles             |
                                                                +-------------------------+

3. Proposed Monorepo Structure
To keep things organized, we will use the following directory structure:

/
├── agents/
│   ├── order-bot/
│   │   └── spec.yaml       <-- Definition for an "order-bot" agent
│   └── sre-assistant/
│       └── spec.yaml       <-- Definition for an "SRE assistant" agent
│
├── factory/
│   ├── src/                <-- Source code for the factory logic (e.g., Python/Go script)
│   └── iac/                <-- Reusable AWS CDK constructs for building agents
│
└── pipeline/
    └── buildspec.yml       <-- Definition for the CI/CD pipeline steps

4. V1 Agent Specification (spec.yaml)
To start, we will keep the agent specification simple. The factory will look for a spec.yaml file with the following content:

# agents/sre-assistant/spec.yaml

# Version of the spec format
apiVersion: factory.agent.v1

# Metadata for the agent
metadata:
  name: sre-assistant
  description: "An agent to help SREs with initial diagnostics."

# Bedrock Agent configuration
spec:
  foundationModelId: "anthropic.claude-3-sonnet-20240229-v1:0" # The FM to use
  # For V1, the action group is not defined here. The factory will automatically
  # attach a default "hello-world" action group to every new agent.

5. The Iterative Plan
We will build this system in small, manageable steps.

Sprint 1 (Our Current Goal):

Set up the monorepo structure in GitHub.

Build the core factory logic in the /factory/iac directory using AWS CDK.

This initial factory will be capable of reading a spec.yaml file and deploying a basic Bedrock Agent.

Crucially, for every agent it creates, the factory will also create and attach a single, predefined "Hello World" Action Group. This action group will be powered by a simple AWS Lambda function written in Go, satisfying the goal of integrating Go with Lambda.

Sprint 2 (Next Steps):

Enhance the spec.yaml to allow developers to define their own custom Action Groups.

The factory will then dynamically create the specified Lambda functions and attach them to the agent.

Sprint 3 (Future):

Add support for defining and attaching Knowledge Bases to agents directly from the spec.yaml.

This V2 blueprint provides a clear and actionable path forward. Let me know if this plan aligns with your vision, and we can prepare to write the first pieces of code.