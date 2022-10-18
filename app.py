#!/usr/bin/env python3
import os
from aws_cdk import (
    Environment,
    aws_ec2 as ec2,
    aws_rds as rds,
    Fn, App, RemovalPolicy, Stack
)
from aws_cdk import Aspects
from cdk_nag import AwsSolutionsChecks, NagSuppressions


# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from datahub_aws.eks_stack import EKSClusterStack
from datahub_aws.es_stack import esstack
from datahub_aws.msk_stack import KafkaStack
from datahub_aws.rds_stack import MySql
app = App()

cdk_environment = Environment(
    account=app.node.try_get_context("ACCOUNT_ID"),
    region=app.node.try_get_context("REGION")
)
resource_prefix = 'datahub'

eks_stack = EKSClusterStack(
                        app,
                        f'EKS',
                        env=cdk_environment,
                        resource_prefix=resource_prefix
                        )
vpc = eks_stack.eks_vpc
security_grp =eks_stack.security_grp

rds_stack = MySql(
                   app, 
                   f'MySql',
                   env=cdk_environment,
                   description="MySQL Instance Stack",
                   vpc =vpc,
                   security_grp =security_grp,
                   db_name="db1",
                   resource_prefix=resource_prefix)
es_stack =  esstack(
                     app, 
                     f'ElasticSearch',
                     env=cdk_environment,
                     description="ES Instance Stack",
                     vpc =vpc,
                     security_grp =security_grp,
                     resource_prefix=resource_prefix)
msk_stack = KafkaStack(
                       app,
                       f'MSK',
                       env=cdk_environment,
                       vpc =vpc,
                       security_grp =security_grp,
                       resource_prefix=resource_prefix)             
                    


# Aspects.of(app).add(AwsSolutionsChecks())
# NagSuppressions.add_stack_suppressions(
# eks_stack, [{"id": "AwsSolutions-IAM4", "reason": "TODO: Stop using AWS managed policies."}]
# )
# NagSuppressions.add_stack_suppressions(
# rds_stack, [{"id": "AwsSolutions-RDS3", "reason": "TODO: No MultiAZ"}]
# )

app.synth()
