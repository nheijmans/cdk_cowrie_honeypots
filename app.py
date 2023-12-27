#!/usr/bin/env python3

from aws_cdk import App

from cdk_cowrie_honeypots.cdk_cowrie_honeypots_stack import CdkCowrieHoneypotsStack
from cdk_confluence_honeypots.cdk_confluence_honeypots_stack import CdkHpConfluenceHoneypotsStack


app = App()
CdkCowrieHoneypotsStack(app, "cdk-cowrie-honeypots")
CdkHpConfluenceHoneypotsStack(app, "cdk-confluence-honeypots")
app.synth()
