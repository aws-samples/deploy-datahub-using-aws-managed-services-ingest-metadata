#new branch

# import modules
import os
import io


from aws_cdk import App, Stack, Environment, CfnOutput, RemovalPolicy

from aws_cdk import (
   
    aws_msk as msk,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_s3_assets as assets,
    aws_msk_alpha as msk_aplha
    
)


from constructs import Construct
KAFKA_DOWNLOAD_VERSION =  "kafka_2.12-2.4.0"
KAFKA_BROKER_NODES =  3
KAFKA_VERSION = '2.6.2'
KAFKA_INSTANCE_TYPE = "kafka.m5.large"
#kafka.t3.small

    


class KafkaStack(Stack):
    def __init__(
        self, scope: Construct, id: str, vpc: ec2.Vpc, security_grp:ec2.SecurityGroup,resource_prefix, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

       
       
        cluster = msk_aplha.Cluster(self, f'MSK',
            cluster_name=f'MSK-{resource_prefix}',
            kafka_version=msk_aplha.KafkaVersion.V2_8_1,
            vpc=vpc,
            encryption_in_transit=msk_aplha.EncryptionInTransitConfig(
                client_broker=msk_aplha.ClientBrokerEncryption.PLAINTEXT
            ),
            security_groups=[security_grp],
            removal_policy= RemovalPolicy.DESTROY,
        )