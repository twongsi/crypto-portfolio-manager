# What is this?
A bot that re-balances my cryptocurrency portfolio once a week

# How does it work?
Every Sunday night:
1. Scrape market cap data from https://nomics.com
1. Choose the top 5 largest market cap cryptocurrencies that are traded on Coinbase Pro
1. Update my portfolio holdings to hold an equal dollar amount of each cryptocurrency (ie, 20% each)

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