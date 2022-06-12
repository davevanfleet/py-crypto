# Crypto Bot

This project is a python script that is used to automate cryptocurrency trading.  It connects to an account in Kraken, runs a technical analysis (RSI) of a selected list of coins, and places buy/sell orders in kraken based on those analyses and the current holdings in your wallet.

## Installation

- Fork and Clone this repo
- `pip3 install -r requirements.txt`
- Create a `.env` file with your kraken api keys (`KRAKEN_API_PUB_KEY` and `KRAKEN_API_SEC_KEY`)

## Usage

This script was built to be run as a daily cron job. Running the `app.py` script is all that is required.
The list of coins selected is fairly conservative.  If you would like to add more coins for your installation simply add them to the `COINS` list in `app.py` using the abbreviations from Kraken.