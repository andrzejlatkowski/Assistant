import asyncio
import datetime
from text_to_speach import play_audio
import yfinance as yf


def fetch_stock_data(ticker_symbol, days_ago):

    ticker_data = yf.Ticker(ticker_symbol)
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days_ago)
    start_date_str = start_date.strftime('%Y-%m-%d')
    historical_data = ticker_data.history(period='1d', start=start_date_str)
    return historical_data

async def speak_stock_data(ticker_symbol, days_ago):

    print(ticker_symbol, days_ago)
    ticker_df = fetch_stock_data(ticker_symbol, days_ago)
    if ticker_df is not None and not ticker_df.empty:
        first_row = ticker_df.head(1)
        formatted_data = first_row[['Open', 'High', 'Low', 'Close']].round(2)

        formatted_str = ""
        for index, row in formatted_data.iterrows():
            formatted_str += f"Open - {row['Open']}, High - {row['High']}, Low - {row['Low']}, Close - {row['Close']}\n"

        if formatted_str:
            print(formatted_str)
            await asyncio.to_thread(play_audio, formatted_str)
        else:
            await asyncio.to_thread(play_audio, "No data available for the specified ticker symbol or days")
    else:
        await asyncio.to_thread(play_audio, "No data available for the specified ticker symbol or days")



async def check():
    ticker_symbol = 'aapl'
    days_ago = 1
    await speak_stock_data(ticker_symbol, days_ago)


# testing
# asyncio.run(check())