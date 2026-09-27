import sqlite3
import statistics
from pathlib import Path


# ==================================================
# DATABASE
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_DIR / "data" / "database" / "market.db"

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()


# ==================================================
# DATASET OVERVIEW
# ==================================================

total_observations = cursor.execute("""
    SELECT COUNT(*)
    FROM market_quotes
""").fetchone()[0]

symbols = cursor.execute("""
    SELECT DISTINCT symbol
    FROM market_quotes
    ORDER BY symbol
""").fetchall()

symbols = [row[0] for row in symbols]

first_timestamp = cursor.execute("""
    SELECT MIN(timestamp)
    FROM market_quotes
""").fetchone()[0]

last_timestamp = cursor.execute("""
    SELECT MAX(timestamp)
    FROM market_quotes
""").fetchone()[0]


# ==================================================
# HEADER
# ==================================================

print()
print("=" * 70)
print("                    MARKET SURVEILLANCE")
print("                         ANALYSIS")
print("=" * 70)

print(f"Total observations:  {total_observations}")
print(f"Stocks monitored:    {', '.join(symbols)}")
print(f"First observation:   {first_timestamp}")
print(f"Last observation:    {last_timestamp}")

print("=" * 70)


# ==================================================
# STORE RESULTS FOR COMPARISON
# ==================================================

stock_results = []


# ==================================================
# ANALYZE EACH STOCK
# ==================================================

for symbol in symbols:

    # --------------------------------------------------
    # BASIC PRICE STATISTICS
    # --------------------------------------------------

    observations, minimum, maximum, average = cursor.execute("""
        SELECT
            COUNT(*),
            MIN(price),
            MAX(price),
            AVG(price)
        FROM market_quotes
        WHERE symbol = ?
    """, (symbol,)).fetchone()


    # --------------------------------------------------
    # FIRST PRICE
    # --------------------------------------------------

    first_price = cursor.execute("""
        SELECT price
        FROM market_quotes
        WHERE symbol = ?
        ORDER BY timestamp ASC
        LIMIT 1
    """, (symbol,)).fetchone()[0]


    # --------------------------------------------------
    # LAST PRICE
    # --------------------------------------------------

    last_price = cursor.execute("""
        SELECT price
        FROM market_quotes
        WHERE symbol = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (symbol,)).fetchone()[0]


    # --------------------------------------------------
    # ALL PRICES IN CHRONOLOGICAL ORDER
    # --------------------------------------------------

    rows = cursor.execute("""
        SELECT price
        FROM market_quotes
        WHERE symbol = ?
        ORDER BY timestamp ASC
    """, (symbol,)).fetchall()

    prices = [row[0] for row in rows]


    # ==================================================
    # PERFORMANCE
    # ==================================================

    price_change = last_price - first_price

    percentage_change = (
        price_change / first_price
    ) * 100


    # ==================================================
    # RETURNS
    # ==================================================

    returns = []

    for i in range(1, len(prices)):

        previous_price = prices[i - 1]
        current_price = prices[i]

        if previous_price != 0:

            return_value = (
                (current_price - previous_price)
                / previous_price
            )

            returns.append(return_value)


    # ==================================================
    # VOLATILITY
    # ==================================================

    if len(returns) > 1:
        volatility = statistics.stdev(returns) * 100
    else:
        volatility = 0


    # ==================================================
    # LARGEST MOVEMENTS
    # ==================================================

    if returns:

        largest_upward_move = max(returns) * 100
        largest_downward_move = min(returns) * 100
        largest_absolute_move = max(
            returns,
            key=abs
        ) * 100

    else:

        largest_upward_move = 0
        largest_downward_move = 0
        largest_absolute_move = 0


    # ==================================================
    # SAVE RESULTS
    # ==================================================

    stock_results.append({
        "symbol": symbol,
        "observations": observations,
        "starting_price": first_price,
        "ending_price": last_price,
        "lowest_price": minimum,
        "highest_price": maximum,
        "average_price": average,
        "price_change": price_change,
        "percentage_change": percentage_change,
        "volatility": volatility,
        "largest_upward_move": largest_upward_move,
        "largest_downward_move": largest_downward_move,
        "largest_absolute_move": largest_absolute_move
    })


    # ==================================================
    # PRINT STOCK ANALYSIS
    # ==================================================

    print()
    print("-" * 70)
    print(f"                         {symbol}")
    print("-" * 70)

    print()
    print("OBSERVATIONS")
    print(f"Number of observations: {observations}")

    print()
    print("PRICE")
    print(f"Starting price:         ${first_price:.2f}")
    print(f"Ending price:           ${last_price:.2f}")
    print(f"Lowest price:           ${minimum:.2f}")
    print(f"Highest price:          ${maximum:.2f}")
    print(f"Average price:          ${average:.2f}")

    print()
    print("PERFORMANCE")
    print(f"Absolute change:        ${price_change:+.2f}")
    print(f"Percentage change:      {percentage_change:+.2f}%")

    print()
    print("VOLATILITY")
    print(f"Return volatility:      {volatility:.4f}%")

    print()
    print("LARGEST MOVEMENTS")
    print(f"Largest upward move:    {largest_upward_move:+.4f}%")
    print(f"Largest downward move:  {largest_downward_move:+.4f}%")
    print(f"Largest absolute move:  {largest_absolute_move:+.4f}%")


# ==================================================
# CROSS-STOCK COMPARISON
# ==================================================

print()
print()
print("=" * 70)
print("                    CROSS-STOCK COMPARISON")
print("=" * 70)

print()
print(
    f"{'STOCK':<8}"
    f"{'RETURN':>12}"
    f"{'VOLATILITY':>15}"
    f"{'LOW':>12}"
    f"{'HIGH':>12}"
)

print("-" * 70)

for result in stock_results:

    print(
        f"{result['symbol']:<8}"
        f"{result['percentage_change']:>+11.2f}%"
        f"{result['volatility']:>14.4f}%"
        f"${result['lowest_price']:>10.2f}"
        f"${result['highest_price']:>10.2f}"
    )


# ==================================================
# CLOSE
# ==================================================

connection.close()

print()
print("=" * 70)
print("                     ANALYSIS COMPLETE")
print("=" * 70)