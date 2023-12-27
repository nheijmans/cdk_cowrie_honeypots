from aws_cdk import (
    Stack,
    aws_ec2 as ec2, 
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_logs as logs
)

from constructs import Construct


class CdkHpConfluenceHoneypotsStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the VPC for the honeypot(s)
        vpc = ec2.Vpc(self, "HoneypotVpc", max_azs=3)     # default is all AZs in region

        # Create the ECS cluster where fargate can deploy the Docker containers
        cluster = ecs.Cluster(self, "HoneypotCluster", vpc=vpc) 

        # Define task definition for Fargate Service
        task_definition = ecs.FargateTaskDefinition(self, "HoneypotTasks", cpu=256, memory_limit_mib=512)

        # Container definition
        confluence_container = ecs.ContainerDefinition(self, "HoneypotConfluenceDefinition",
            image=ecs.ContainerImage.from_registry("statixs/confluence-pot"), 
            task_definition=task_definition,
            logging=ecs.AwsLogDriver(
                stream_prefix="hpconfluence",
                log_retention=logs.RetentionDays.ONE_DAY,
            ),
        )

        # ECS Security Group definition
        sg_app = ec2.SecurityGroup(self, "honeypot-sg-http", vpc=vpc, description="Allow traffic to the honeypot")
        sg_app.add_ingress_rule(ec2.Peer.ipv4("10.0.0.0/0"), ec2.Port.tcp(8080))

        # Fargate service definition
        fargate_service = ecs.FargateService(self, "HoneypotFargate", cluster=cluster, 
            assign_public_ip=True, 
            desired_count=1, 
            security_groups=[sg_app], 
            task_definition=task_definition
        )
