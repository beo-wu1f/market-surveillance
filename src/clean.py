import sqlite3
from pathlib import Path


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_DIR / "data" / "database" / "market.db"

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()


# --------------------------------------------------
# BASIC DATA QUALITY CHECKS
# --------------------------------------------------

print()
print("=" * 65)
print("                 DATA QUALITY CHECK")
print("=" * 65)


# --------------------------------------------------
# 1. TOTAL RECORDS
# --------------------------------------------------

total_records = cursor.execute("""
    SELECT COUNT(*)
    FROM market_quotes
""").fetchone()[0]

print()
print("1. RECORD COUNT")
print("-" * 65)
print(f"Total records:       {total_records}")


# --------------------------------------------------
# 2. RECORDS PER SYMBOL
# --------------------------------------------------

symbol_counts = cursor.execute("""
    SELECT
        symbol,
        COUNT(*)
    FROM market_quotes
    GROUP BY symbol
    ORDER BY symbol
""").fetchall()

print()
print("2. RECORDS PER STOCK")
print("-" * 65)

for symbol, count in symbol_counts:
    print(f"{symbol:<10} {count}")


# --------------------------------------------------
# 3. NULL VALUES
# --------------------------------------------------

columns = [
    "timestamp",
    "symbol",
    "price",
    "change",
    "change_percent",
    "high",
    "low",
    "open",
    "previous_close"
]

print()
print("3. NULL VALUES")
print("-" * 65)

null_found = False

for column in columns:

    count = cursor.execute(f"""
        SELECT COUNT(*)
        FROM market_quotes
        WHERE {column} IS NULL
    """).fetchone()[0]

    if count > 0:
        null_found = True
        print(f"{column:<18} {count}")

if not null_found:
    print("No NULL values found.")


# --------------------------------------------------
# 4. INVALID PRICES
# --------------------------------------------------

invalid_prices = cursor.execute("""
    SELECT COUNT(*)
    FROM market_quotes
    WHERE price IS NULL
       OR price <= 0
""").fetchone()[0]

print()
print("4. INVALID PRICES")
print("-" * 65)
print(f"Invalid prices:     {invalid_prices}")


# --------------------------------------------------
# 5. INVALID HIGH / LOW RELATIONSHIPS
# --------------------------------------------------

invalid_ranges = cursor.execute("""
    SELECT COUNT(*)
    FROM market_quotes
    WHERE high < low
""").fetchone()[0]

print()
print("5. PRICE RANGE CHECK")
print("-" * 65)
print(f"High < Low records: {invalid_ranges}")


# --------------------------------------------------
# 6. PRICE OUTSIDE DAILY RANGE
# --------------------------------------------------

outside_range = cursor.execute("""
    SELECT COUNT(*)
    FROM market_quotes
    WHERE price < low
       OR price > high
""").fetchone()[0]

print()
print("6. CURRENT PRICE RANGE CHECK")
print("-" * 65)
print(f"Price outside range: {outside_range}")


# --------------------------------------------------
# 7. DUPLICATE RECORDS
# --------------------------------------------------

duplicates = cursor.execute("""
    SELECT
        timestamp,
        symbol,
        COUNT(*)
    FROM market_quotes
    GROUP BY timestamp, symbol
    HAVING COUNT(*) > 1
""").fetchall()

print()
print("7. DUPLICATES")
print("-" * 65)

if duplicates:
    print(f"Duplicate timestamp/symbol combinations: {len(duplicates)}")

    for row in duplicates[:10]:
        print(row)

else:
    print("No duplicate timestamp/symbol combinations found.")


# --------------------------------------------------
# 8. TIMESTAMP RANGE
# --------------------------------------------------

first_timestamp = cursor.execute("""
    SELECT MIN(timestamp)
    FROM market_quotes
""").fetchone()[0]

last_timestamp = cursor.execute("""
    SELECT MAX(timestamp)
    FROM market_quotes
""").fetchone()[0]

print()
print("8. TIMESTAMP RANGE")
print("-" * 65)
print(f"First observation:   {first_timestamp}")
print(f"Last observation:    {last_timestamp}")


# --------------------------------------------------
# 9. FINAL SUMMARY
# --------------------------------------------------

print()
print("=" * 65)
print("                 QUALITY CHECK COMPLETE")
print("=" * 65)

issues = (
    invalid_prices
    + invalid_ranges
    + outside_range
    + len(duplicates)
)

if issues == 0:
    print("Status:              DATA LOOKS CLEAN")
else:
    print(f"Potential issues:    {issues}")

print()
print("No database records were modified.")
print("=" * 65)


connection.close()