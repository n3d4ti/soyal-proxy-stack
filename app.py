#!/usr/bin/env python3

from aws_cdk import core

from soyal_proxy_stack.soyal_proxy_stack_stack import SoyalProxyStackStack


app = core.App()
SoyalProxyStackStack(app, "soyal-proxy-stack")

app.synth()
