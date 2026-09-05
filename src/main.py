import os
import finnhub
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")

client = finnhub.Client(api_key=API_KEY)

quote = client.quote("AAPL")

print(quote)