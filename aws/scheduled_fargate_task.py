from typing import Mapping

from aws_cdk.aws_applicationautoscaling import Schedule
from aws_cdk.aws_ecs import ContainerImage, AwsLogDriver
from aws_cdk.aws_ecs_patterns import ScheduledFargateTask, ScheduledFargateTaskImageOptions
from aws_cdk.aws_logs import LogGroup
from aws_cdk.core import Construct


def scheduled_fargate_task(scope: Construct, _id: str, image: ContainerImage, module: str,
                           environment: Mapping[str, str], schedule: Schedule, log_prefix: str) -> ScheduledFargateTask:
    return ScheduledFargateTask(
        scope,
        _id,
        schedule=schedule,
        scheduled_fargate_task_image_options=ScheduledFargateTaskImageOptions(
            image=image,
            command=['pipenv', 'run', 'python', '-u', '-m', module],
            environment=environment,
            log_driver=AwsLogDriver(
                stream_prefix=log_prefix,
                log_group=LogGroup(scope, '%sLogGroup' % _id)
            ),
            cpu=256,
            memory_limit_mib=512
        )
    )
