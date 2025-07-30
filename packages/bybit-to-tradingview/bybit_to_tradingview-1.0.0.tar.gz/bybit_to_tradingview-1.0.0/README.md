# bybit-to-tradingview

A simple Python CLI tool that fetches the top 40 USDT perpetual trading pairs from Bybit  
and exports them in a format compatible with TradingView's symbol search.

## Features

- Uses Bybit's public API
- Sorts instruments by 24h trading volume
- Outputs `BYBIT:<symbol>` format for use in TradingView
- Written in Python 3

## Usage

After installation:

```bash
bybit-to-tradingview
