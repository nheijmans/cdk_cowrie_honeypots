#!/usr/bin/env python3

from aws_cdk import core

from cdk_cowrie_honeypots.cdk_cowrie_honeypots_stack import CdkCowrieHoneypotsStack


app = core.App()
CdkCowrieHoneypotsStack(app, "cdk-cowrie-honeypots")

app.synth()
