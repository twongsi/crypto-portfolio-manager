from os import getcwd, environ

from aws_cdk.aws_applicationautoscaling import Schedule
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.core import Stack, Construct, App, Environment
from aws.scheduled_fargate_task import scheduled_fargate_task


class MainStack(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        image = ContainerImage.from_asset(
            getcwd(),
            file='Dockerfile',
            repository_name='crypto-portfolio-manager',
            exclude=['cdk.out']
        )
        scheduled_fargate_task(
            scope,
            'AggressivePortfolioManager',
            image=image,
            module='src.aggressive_portfolio.rebalance',
            environment={
                'COINBASE_PRO_API_KEY': environ.get('AGGRESSIVE_PORTFOLIO_KEY'),
                'COINBASE_PRO_API_SECRET': environ.get('AGGRESSIVE_PORTFOLIO_SECRET'),
                'COINBASE_PRO_API_PASSPHRASE': environ.get('AGGRESSIVE_PORTFOLIO_PASSPHRASE'),
                'N_PORTFOLIO_HOLDINGS': '5'
            },
            schedule=Schedule.cron(
                minute='0',
                hour='2',
                week_day='MON'
            ),
            log_prefix='aggressive-portfolio-manager'
        )
        scheduled_fargate_task(
            scope,
            'MarketCapPortfolioManager',
            image=image,
            module='src.market_cap_portfolio.rebalance',
            environment={
                'COINBASE_PRO_API_KEY': environ.get('MARKET_CAP_PORTFOLIO_KEY'),
                'COINBASE_PRO_API_SECRET': environ.get('MARKET_CAP_PORTFOLIO_SECRET'),
                'COINBASE_PRO_API_PASSPHRASE': environ.get('MARKET_CAP_PORTFOLIO_PASSPHRASE')
            },
            schedule=Schedule.cron(
                minute='0',
                hour='2',
                day='1'
            ),
            log_prefix='market-cap-portfolio-manager'
        )


if __name__ == '__main__':
    app = App()
    MainStack(app, 'CryptoPortfolioManager', env=Environment(region=environ.get('AWS_DEFAULT_REGION')))
    app.synth()
