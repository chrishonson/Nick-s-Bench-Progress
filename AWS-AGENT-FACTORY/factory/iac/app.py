#!/usr/bin/env python3
import os

import aws_cdk as cdk

from iac.iac_stack import IacStack


app = cdk.App()

env = cdk.Environment(account="717915633540", region="us-east-1")

IacStack(app, "IacStack", env=env)

app.synth()