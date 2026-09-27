import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import finnhub
from dotenv import load_dotenv

from database import create_database, insert_quote


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")
client = finnhub.Client(api_key=API_KEY)

symbols = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN"
]

INTERVAL = 60              # seconds between collection cycles
DURATION = 2 * 60 * 60     # 2 hours


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

create_database()


# --------------------------------------------------
# COLLECTION
# --------------------------------------------------

start_time = time.time()

print("=" * 65)
print("                 MARKET DATA COLLECTOR")
print("=" * 65)
print(f"Stocks:       {', '.join(symbols)}")
print(f"Interval:     {INTERVAL} seconds")
print(f"Duration:     2 hours")
print("Failure mode: Skip failed requests and continue")
print("Press CTRL + C to stop.")
print("=" * 65)


while time.time() - start_time < DURATION:

    timestamp = datetime.now(ZoneInfo("Asia/Kolkata"))

    successful = 0
    failed = 0

    print()
    print(
        f"Collection time: "
        f"{timestamp.strftime('%Y-%m-%d %H:%M:%S IST')}"
    )

    for symbol in symbols:

        try:
            quote = client.quote(symbol)

            # Make sure Finnhub actually returned a usable quote.
            if not quote or quote.get("c") is None:
                raise ValueError("Invalid or empty quote returned")

            insert_quote(
                timestamp.isoformat(),
                symbol,
                quote
            )

            successful += 1

            print(
                f"{symbol:<6} | "
                f"${quote['c']:.2f} | "
                f"{quote['dp']:+.2f}% | "
                f"SAVED"
            )

        except Exception as error:

            failed += 1

            print(
                f"{symbol:<6} | "
                f"ERROR | "
                f"{type(error).__name__}: {error}"
            )

    print("-" * 65)
    print(
        f"Cycle result: "
        f"{successful} saved | "
        f"{failed} failed"
    )

    time.sleep(INTERVAL)


# --------------------------------------------------
# COMPLETE
# --------------------------------------------------

print()
print("=" * 65)
print("                 COLLECTION COMPLETE")
print("=" * 65)
print("The 2-hour collection period has ended.")
print("Successful observations were preserved in SQLite.")
print("Failed requests were skipped.")
print("=" * 65)