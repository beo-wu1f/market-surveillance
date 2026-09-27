import os
from datetime import datetime, timezone

import finnhub
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")

client = finnhub.Client(api_key=API_KEY)

# --------------------------------------------------
# TEST SETTINGS
# --------------------------------------------------

symbols = ["AAPL", "MSFT", "NVDA", "AMZN"]

resolution = "5"

start_date = datetime(2026, 9, 14, tzinfo=timezone.utc)
end_date = datetime(2026, 9, 19, tzinfo=timezone.utc)

start_timestamp = int(start_date.timestamp())
end_timestamp = int(end_date.timestamp())

# --------------------------------------------------
# DISPLAY TEST INFORMATION
# --------------------------------------------------

print()
print("=" * 65)
print("             FINNHUB HISTORICAL DATA TEST")
print("=" * 65)

print(f"Date range:   September 14 -> September 18, 2026")
print(f"Resolution:   {resolution}-minute candles")
print(f"Stocks:       {', '.join(symbols)}")

print("=" * 65)

# --------------------------------------------------
# RETRIEVE DATA
# --------------------------------------------------

for symbol in symbols:

    print()
    print(f"Retrieving {symbol}...")

    try:
        data = client.stock_candles(
            symbol,
            resolution,
            start_timestamp,
            end_timestamp
        )

        print(f"Status:       {data.get('s', 'UNKNOWN')}")

        if data.get("s") != "ok":
            print(f"ERROR:        {data}")
            continue

        timestamps = data.get("t", [])
        opens = data.get("o", [])
        highs = data.get("h", [])
        lows = data.get("l", [])
        closes = data.get("c", [])
        volumes = data.get("v", [])

        print(f"Candles:      {len(timestamps)}")

        if timestamps:
            first_time = datetime.fromtimestamp(
                timestamps[0],
                tz=timezone.utc
            )

            last_time = datetime.fromtimestamp(
                timestamps[-1],
                tz=timezone.utc
            )

            print(f"First candle: {first_time}")
            print(f"Last candle:  {last_time}")

        print(f"Open values:  {len(opens)}")
        print(f"Close values: {len(closes)}")
        print(f"Volume rows:  {len(volumes)}")

        print()
        print("First 3 candles:")

        for i in range(min(3, len(timestamps))):
            candle_time = datetime.fromtimestamp(
                timestamps[i],
                tz=timezone.utc
            )

            print(
                f"{candle_time} | "
                f"O={opens[i]:.2f} "
                f"H={highs[i]:.2f} "
                f"L={lows[i]:.2f} "
                f"C={closes[i]:.2f} "
                f"V={volumes[i]}"
            )

    except Exception as error:

        print(f"ERROR: {type(error).__name__}")
        print(error)

print()
print("=" * 65)
print("                 TEST COMPLETE")
print("=" * 65)