'''
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
'''
#new branch

from aws_cdk import App, Stack, Environment, CfnOutput, RemovalPolicy
from aws_cdk import (
    SecretValue,
    aws_opensearchservice as opensearch,
    aws_iam as iam, 
    aws_ec2 as ec2, 
    Stack
)
from aws_cdk.aws_s3_assets import Asset

import fileinput
import json
import os
import random
import string
import sys

from constructs import Construct

# Lambda Interval Settings (seconds)
LAMBDA_INTERVAL=300

# OpenSearch and Dashboards specific constants 

DOMAIN_ADMIN_UNAME='opensearch'
DOMAIN_ADMIN_PW=''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(13)) + random.choice(string.ascii_lowercase) + random.choice(string.ascii_uppercase) + random.choice(string.digits) + "!" 
DOMAIN_DATA_NODE_INSTANCE_TYPE='m6g.large.search'
DOMAIN_DATA_NODE_INSTANCE_COUNT=2
DOMAIN_INSTANCE_VOLUME_SIZE=100
DOMAIN_AZ_COUNT=2



DOMAIN_MASTER_NODE_INSTANCE_TYPE='c6g.large.search'
DOMAIN_MASTER_NODE_INSTANCE_COUNT=0


DOMAIN_UW_NODE_INSTANCE_TYPE='ultrawarm1.medium.search'
DOMAIN_UW_NODE_INSTANCE_COUNT=0



class esstack(Stack):
    def __init__(self, scope: Construct, id: str,vpc: ec2.Vpc, 
                security_grp:ec2.SecurityGroup,resource_prefix:str ,**kwargs) -> None:
        super().__init__(scope, id, **kwargs)

       

        domain = opensearch.Domain(self, f'opensearch', 
            version=opensearch.EngineVersion.ELASTICSEARCH_7_10, # Upgrade when CDK upgrades
            domain_name=f'opensearch-domain-{resource_prefix}',
            removal_policy=RemovalPolicy.DESTROY,
            capacity=opensearch.CapacityConfig(
                data_node_instance_type=DOMAIN_DATA_NODE_INSTANCE_TYPE,
                data_nodes=DOMAIN_DATA_NODE_INSTANCE_COUNT,
                master_node_instance_type=DOMAIN_MASTER_NODE_INSTANCE_TYPE,
                master_nodes=DOMAIN_MASTER_NODE_INSTANCE_COUNT,
                warm_instance_type=DOMAIN_UW_NODE_INSTANCE_TYPE,
                warm_nodes=DOMAIN_UW_NODE_INSTANCE_COUNT
            ),
            ebs=opensearch.EbsOptions(
                enabled=True,
                volume_size=DOMAIN_INSTANCE_VOLUME_SIZE,
                volume_type=ec2.EbsDeviceVolumeType.GP2
            ),
            vpc=vpc,
            security_groups=[security_grp],
            zone_awareness=opensearch.ZoneAwarenessConfig(
                enabled=True,
                availability_zone_count=DOMAIN_AZ_COUNT
            ),
            enforce_https=True,
            node_to_node_encryption=True,
            encryption_at_rest={
                "enabled": True
            },
            use_unsigned_basic_auth=True,
            fine_grained_access_control={
                "master_user_name": DOMAIN_ADMIN_UNAME,
                "master_user_password": SecretValue.plain_text(DOMAIN_ADMIN_PW)
                
            }
        )
#   plain_text  -> unsafe_plain_text
        CfnOutput(self, "MasterUser",
                        value=DOMAIN_ADMIN_UNAME,
                        description="Master User Name for Amazon OpenSearch Service")

        CfnOutput(self, "MasterPW",
                        value=DOMAIN_ADMIN_PW,
                        description="Master User Password for Amazon OpenSearch Service")

      