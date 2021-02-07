# What is this?
A bot that re-balances my cryptocurrency portfolio once a month

# How does it work?
At the beginning of every month:
1. Scrape market cap & price history data from https://nomics.com
1. Choose the top `N_TO_HOLD` largest market cap cryptocurrencies that are traded on Coinbase Pro
1. Update my portfolio to hold the cryptocurrencies from the previous step, weighted by their inverse volatility

# Requirements
- Python 3.8.x
- Pipenv

# To Run Locally
(see `Makefile`)

# Environment Variables
| Key | Description|
|---|---|
| COINBASE_PRO_API_KEY | Provided by Coinbase Pro |
| COINBASE_PRO_API_SECRET | Provided by Coinbase Pro |
| COINBASE_PRO_API_PASSPHRASE | Provided by Coinbase Pro |
| N_TO_HOLD | Number of cryptocurrencies to hold in your portfolio |
| EMAIL | Email address to send rebalance completion notification to |

# Reference
- Inspiration for re-balance weighting strategy: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3454764
  - "Inverse Volatility" strategy was chosen due to its relative ease of implementation
- Crypto trading platform of choice: https://pro.coinbase.com/
- Coinbase Pro python client: https://github.com/danpaquin/coinbasepro-python
- Crypto data scraped from https://nomics.com

# TODO
- Make re-balancing logic more transaction-efficient than just blindly liquidating all holdings and then re-buying so that Coinbase Pro fees don't kill me