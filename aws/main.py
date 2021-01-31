import os

from aws_cdk.aws_applicationautoscaling import Schedule
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.core import Stack, Construct, App, Environment

from aws.env import env
from aws.scheduled_fargate_task import scheduled_fargate_task


class MainStack(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        image = ContainerImage.from_asset(
            os.getcwd(),
            file='Dockerfile',
            repository_name='crypto-portfolio-manager',
            exclude=['cdk.out']
        )
        scheduled_fargate_task(
            scope,
            'AggroPortfolioManager',
            image=image,
            module='src.main',
            environment={
                'COINBASE_PRO_API_KEY': env('AGGRO_PORTFOLIO_KEY'),
                'COINBASE_PRO_API_SECRET': env('AGGRO_PORTFOLIO_SECRET'),
                'COINBASE_PRO_API_PASSPHRASE': env('AGGRO_PORTFOLIO_PASSPHRASE'),
                'N_PORTFOLIO_HOLDINGS': '5'
            },
            schedule=Schedule.cron(
                minute='0',
                hour='2',
                week_day='MON'
            ),
            log_prefix='aggro-portfolio-manager'
        )


if __name__ == '__main__':
    app = App()
    MainStack(app, 'CryptoPortfolioManager', env=Environment(region=env('AWS_DEFAULT_REGION')))
    app.synth()
