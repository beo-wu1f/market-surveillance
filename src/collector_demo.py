import time

print()
print("=" * 65)
print("                 MARKET DATA COLLECTOR")
print("=" * 65)
print("Stocks:    AAPL, MSFT, NVDA, AMZN")
print("Interval:  60 seconds")
print("Duration:  2 hours")
print("Mode:      Demonstration / Screenshot Mode")
print("=" * 65)

cycles = [
    ("2026-09-22 17:24:36 IST", [
        ("AAPL", 338.98, 0.12),
        ("MSFT", 501.61, -0.08),
        ("NVDA", 227.38, 0.15),
        ("AMZN", 258.45, -0.21),
    ]),
    ("2026-09-22 17:25:36 IST", [
        ("AAPL", 339.12, 0.04),
        ("MSFT", 501.42, -0.04),
        ("NVDA", 227.51, 0.06),
        ("AMZN", 258.18, -0.10),
    ]),
]

for timestamp, quotes in cycles:
    print()
    print(f"Collection time: {timestamp}")
    print("-" * 65)

    for symbol, price, change in quotes:
        print(
            f"{symbol:<6} | "
            f"${price:>7.2f} | "
            f"{change:+.2f}% | "
            f"SAVED"
        )

    print("-" * 65)
    print("Cycle result: 4 saved | 0 failed")

print()
print("=" * 65)
print("                 COLLECTION COMPLETE")
print("=" * 65)
print("Demonstration complete.")
print("Note: No API requests were made.")
print("No database records were modified.")
print("=" * 65)