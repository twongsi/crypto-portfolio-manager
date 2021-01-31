import os

from aws_cdk.aws_applicationautoscaling import Schedule
from aws_cdk.aws_ecs import ContainerImage, AwsLogDriver
from aws_cdk.aws_ecs_patterns import ScheduledFargateTask, ScheduledFargateTaskImageOptions
from aws_cdk.aws_logs import LogGroup
from aws_cdk.core import Stack, Construct, App, Environment


def env(key: str) -> str:
    return os.environ.get(key)


class MainStack(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        schedule = Schedule.cron(
            minute='0',
            hour='2',
            week_day='MON'
        )
        image = ContainerImage.from_asset(
            os.getcwd(),
            file='Dockerfile',
            repository_name='crypto-portfolio-manager',
            exclude=['cdk.out']
        )
        log_group = LogGroup(self, 'CryptoPortfolioManagerLogGroup')
        log_driver = AwsLogDriver(
            stream_prefix='crypto-portfolio-manager',
            log_group=log_group
        )
        scheduled_fargate_task_image_options = ScheduledFargateTaskImageOptions(
            image=image,
            command=['pipenv', 'run', 'python', '-u', '-m', 'src.main'],
            environment={
                'COINBASE_PRO_API_PASSPHRASE': env('COINBASE_PRO_API_PASSPHRASE'),
                'COINBASE_PRO_API_SECRET': env('COINBASE_PRO_API_SECRET'),
                'COINBASE_PRO_API_KEY': env('COINBASE_PRO_API_KEY'),
                'N_PORTFOLIO_HOLDINGS': '5'
            },
            log_driver=log_driver,
            cpu=256,
            memory_limit_mib=512
        )
        ScheduledFargateTask(
            self,
            'ScheduledTask',
            schedule=schedule,
            scheduled_fargate_task_image_options=scheduled_fargate_task_image_options
        )


if __name__ == '__main__':
    app = App()
    MainStack(app, 'CryptoPortfolioManager', env=Environment(region=env('AWS_DEFAULT_REGION')))
    app.synth()
