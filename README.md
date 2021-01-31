# What is this?
My attempt at a low-frequency cryptocurrency trading bot.

# How does it work?
Once a week:
1. Scrape 7-day cryptocurrency price predictions from https://nomics.com/
1. Of those price predictions, filter to currencies with positive price prediction that are also traded on Coinbase Pro
1. Re-balance my Coinbase Pro portfolio so that it holds an equal amount of the top `N_PORTFOLIO_HOLDINGS` currencies (if no positive price predictions found in previous step, just don't buy any crypto for the week)

# Required Environment Variables
| Name | Description |
| --- | --- |
| N_PORTFOLIO_HOLDINGS | # of cryptocurrencies to hold in portfolio
| COINBASE_PRO_API_KEY | Provided to you by Coinbase |
| COINBASE_PRO_API_SECRET | Provided to you by Coinbase |
| COINBASE_PRO_API_PASSPHRASE | Provided to you by Coinbase |

# Reference
- Main inspiration for this bot: https://blog.shrimpy.io/blog/case-study-using-machine-learning-for-portfolio-management
- Crypto trading platform of choice: https://pro.coinbase.com/
- Coinbase Pro python client: https://github.com/danpaquin/coinbasepro-python

# TODO
- At the start of each run, send myself an email that includes my current portfolio value as well as the current price of my currently-held currencies
- At the end of each run, send myself an email that re-balancing is done, as well as what my new holdings are (incl. Nomics predictions)
- Make re-balancing logic more transaction-efficient than just blindly liquidating all holdings and then re-buying so that Coinbase Pro fees don't kill me.
- Come up with some weighting scheme that might outperform an equally-balanced portfolio.
- Do my own ML-based price prediction instead of scraping Nomics's data.
