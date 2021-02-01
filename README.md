# What is this?
My attempt at a low-frequency cryptocurrency trading bot.

# How does it work?
This bot automatically rebalances two of my cryptocurrency portfolios for me: an `Aggressive` one based on short-term price predictions, and a `Market Cap` one that holds established large-cap cryptocurrencies

### Aggressive Portfolio
#### Rebalance frequency: Weekly
#### Logic:
1. Scrape 7-day cryptocurrency price predictions from https://nomics.com/
1. Of those price predictions, filter to currencies with positive price prediction that are also traded on Coinbase Pro
1. Re-balance my Coinbase Pro portfolio so that it holds an equal amount of the top `N_PORTFOLIO_HOLDINGS` currencies (if no positive price predictions found in previous step, just don't buy any crypto for the week)

### Market Cap Portfolio
#### Rebalance frequency: Monthly
#### Logic:
1. Scrape market cap data from https://nomics.com/
1. Of those market caps, filter symbols down to large cap (market cap > (mean market cap + std deviation market cap))
1. Re-balance my Coinbase Pro portfolio so that it holds an equal amount of the cryptocurrencies from the previous step

# Requirements
- Python 3.8.x
- Pipenv

# Reference
- Main inspiration for this bot: https://blog.shrimpy.io/blog/case-study-using-machine-learning-for-portfolio-management
- Crypto trading platform of choice: https://pro.coinbase.com/
- Coinbase Pro python client: https://github.com/danpaquin/coinbasepro-python
- Crypto data scraped from https://nomics.com

# TODO
- If Coinbase API rate limits become an issue, implement rate-limiting/retrying in `CoinbaseProApi`
- At the end of each run, send myself an email that re-balancing is done, as well as what my new holdings are (incl. Nomics predictions)
- Make re-balancing logic more transaction-efficient than just blindly liquidating all holdings and then re-buying so that Coinbase Pro fees don't kill me
- Come up with some weighting scheme that might outperform an equally-balanced portfolio
- Do my own ML-based price prediction instead of scraping Nomics's data
