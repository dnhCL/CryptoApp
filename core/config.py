from dotenv import load_dotenv
import os
from binance.spot import Spot

load_dotenv()

def crear_cliente():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    return Spot(api_key=api_key, api_secret=api_secret)
