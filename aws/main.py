from os import getcwd, environ

from aws_cdk.aws_applicationautoscaling import Schedule
from aws_cdk.aws_ecs import ContainerImage, AwsLogDriver
from aws_cdk.aws_ecs_patterns import ScheduledFargateTask, ScheduledFargateTaskImageOptions
from aws_cdk.aws_logs import LogGroup
from aws_cdk.core import Stack, Construct, App, Environment


class MainStack(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        ScheduledFargateTask(
            self,
            _id,
            schedule=Schedule.cron(
                minute='0',
                hour='6',
                week_day='MON'
            ),
            scheduled_fargate_task_image_options=ScheduledFargateTaskImageOptions(
                image=ContainerImage.from_asset(
                    getcwd(),
                    file='Dockerfile',
                    repository_name='crypto-portfolio-manager',
                    exclude=['cdk.out']
                ),
                command=['pipenv', 'run', 'python', '-u', '-m', 'src.main'],
                environment={
                    'COINBASE_PRO_API_KEY': environ.get('COINBASE_PRO_API_KEY'),
                    'COINBASE_PRO_API_SECRET': environ.get('COINBASE_PRO_API_SECRET'),
                    'COINBASE_PRO_API_PASSPHRASE': environ.get('COINBASE_PRO_API_PASSPHRASE'),
                    'EMAIL': environ.get('EMAIL'),
                    'N_TO_HOLD': '10'
                },
                log_driver=AwsLogDriver(
                    stream_prefix='crypto-portfolio-manager',
                    log_group=LogGroup(self, '%sLogGroup' % _id)
                ),
                cpu=256,
                memory_limit_mib=512
            )
        )


if __name__ == '__main__':
    app = App()
    MainStack(app, 'CryptoPortfolioManager', env=Environment(region=environ.get('AWS_DEFAULT_REGION')))
    app.synth()
