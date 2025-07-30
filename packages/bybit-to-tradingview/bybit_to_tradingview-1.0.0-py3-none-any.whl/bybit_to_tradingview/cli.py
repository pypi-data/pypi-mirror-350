import requests

# URLs
instruments_url = "https://api.bybit.com/v5/market/instruments-info?category=linear"
tickers_url = "https://api.bybit.com/v5/market/tickers?category=linear"
output_file = "bybit_futures_tradingview_symbols.txt"

def main():
    try:
        # Fetch instrument list
        response_instruments = requests.get(instruments_url)
        response_instruments.raise_for_status()
        instruments_data = response_instruments.json()

        if instruments_data.get("result") and instruments_data["result"].get("list"):
            instruments = instruments_data["result"]["list"]
        else:
            print("No instrument data found.")
            return

        # Fetch volume data
        response_tickers = requests.get(tickers_url)
        response_tickers.raise_for_status()
        tickers_data = response_tickers.json()

        if tickers_data.get("result") and tickers_data["result"].get("list"):
            tickers = tickers_data["result"]["list"]
        else:
            print("No ticker data found.")
            return

        # Create a dictionary for quick lookup of volume
        volume_map = {item["symbol"]: float(item["volume24h"]) for item in tickers}

        # Sort symbols by volume
        instruments.sort(key=lambda x: volume_map.get(x["symbol"], 0), reverse=True)

        # Write top 40 symbols to output file
        with open(output_file, "w") as f:
            for instrument in instruments[:40]:
                symbol = instrument["symbol"]
                f.write(f"BYBIT:{symbol}\n")

        print(f"Top 40 symbols saved to {output_file}")

    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
