#!/usr/bin/env python3

import os
from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds

POSTGRES_PORT = 5432

class MyStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        vpc = ec2.Vpc(self, "VPC")

        vpc_security_group = ec2.SecurityGroup(self, "VPC_Security_Group",
            vpc=vpc,
            description="Security group for VPC",
            allow_all_outbound=True)
        vpc_security_group.connections.allow_from(
                vpc_security_group, 
                ec2.Port.tcp(POSTGRES_PORT),
                "Ingress SSH from public sg");

        # Bastion Host
        instance = ec2.BastionHostLinux(self, "BastionHost",
            instance_type=ec2.InstanceType("t2.micro"),
            vpc = vpc,
            security_group=vpc_security_group)

        # Relational Database
        rds.DatabaseInstance(self, "RDS",
            database_name="AppDb",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_12_3
            ),
            vpc=vpc,
            port=POSTGRES_PORT,
            instance_type= ec2.InstanceType.of(
                ec2.InstanceClass.MEMORY4,
                ec2.InstanceSize.LARGE,
            ),
            security_groups=[vpc_security_group],
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False
        ),

stage = "dev"
app = core.App()
MyStack(app, "pensieve-{}".format(stage))
app.synth()
