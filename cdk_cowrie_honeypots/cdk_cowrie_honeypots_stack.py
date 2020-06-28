from aws_cdk import (
    core, 
    aws_ec2 as ec2, 
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_logs as logs
)

class CdkCowrieHoneypotsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the VPC for the honeypot(s)
        vpc = ec2.Vpc(self, "HoneypotVpc", max_azs=3)     # default is all AZs in region

        # Create the ECS cluster where fargate can deploy the Docker containers
        cluster = ecs.Cluster(self, "HoneypotCluster", vpc=vpc) 

        # Define task definition for Fargate Service
        task_definition = ecs.FargateTaskDefinition(self, "HoneypotTasks", cpu=256, memory_limit_mib=512)

        # Container definition
        container_definition = ecs.ContainerDefinition(self, "HoneypotContainerDefinition",
            #image=ecs.ContainerImage.from_registry("statixs/cowrie"), 
            image=ecs.ContainerImage.from_asset(directory = "docker"),
            task_definition=task_definition,
            stop_timeout=core.Duration.seconds(2),
            logging=ecs.AwsLogDriver(
                stream_prefix="cowrie",
                log_retention=logs.RetentionDays.ONE_WEEK,
            ),
        )

        # ECS Security Group definition
        sg_ssh = ec2.SecurityGroup(self, "honeypot-sg-ssh", vpc=vpc, description="Allow SSH to the honeypot")
        sg_ssh.add_ingress_rule(ec2.Peer.ipv4("0.0.0.0/0"), ec2.Port.tcp(22))

        # Fargate service definition
        fargate_service = ecs.FargateService(self, "HoneypotFargate", cluster=cluster, 
            assign_public_ip=True, 
            desired_count=1, 
            security_group=sg_ssh, 
            task_definition=task_definition,
            platform_version=ecs.FargatePlatformVersion.VERSION1_3
        )
