import yfinance as yf
import pandas as pd

# List of all indexes to be gathered
tickers = ['^DJI', '^GSPC', '^IXIC', '^TNX', 'GC=F', 'CL=F', 'SI=F']

# Initialize list of all values to be gathered
current_prices = []
prev_closes = []
last_weeks_closes = []
daily_changes = []
weekly_changes = []


def get_current_price(tick):
    # Get today's price
    today_data = yf.Ticker.history(tick, period='1d')
    return round(today_data['Close'][0], 2)


def get_last_weeks_close(tick):
    # Get last weeks closing price
    today_data = yf.Ticker.history(tick, period='6d')
    return round(today_data['Close'][0], 2)


def collect_data():
    # Loop through each ticker to get values and organize in data table
    for tick in tickers:
        # Gather all values
        ticker = yf.Ticker(tick)
        current_price = round(get_current_price(ticker), 2)
        prev_close = round(ticker.info['previousClose'], 2)
        last_weeks_close = round(get_last_weeks_close(ticker), 2)
        daily_change = round(current_price - prev_close, 2)
        weekly_change = round(current_price - last_weeks_close, 2)

        # Clean the data
        current_price = "{:,.2f}".format(current_price)
        prev_close = "{:,.2f}".format(prev_close)
        last_weeks_close = "{:,.2f}".format(last_weeks_close)
        daily_change = "{:,.2f}".format(daily_change)
        weekly_change = "{:,.2f}".format(weekly_change)

        # Format Data
        current_prices.append(str(current_price))
        prev_closes.append(str(prev_close))
        last_weeks_closes.append(str(last_weeks_close))
        daily_changes.append(str(daily_change))
        weekly_changes.append(str(weekly_change))

    # Create data table and convert it to HTML
    data_table = pd.DataFrame({'Index': ['Dow Jones', 'S&P 500', 'NASDAQ', 'TNX',
                                         'Gold', 'Crude Oil', 'Silver'],
                               'Current Prices': current_prices,
                               'Prev.Close': prev_closes,
                               "Today's Change": daily_changes,
                               'L.W Change': last_weeks_closes,
                               '1-Week Change': weekly_changes}).to_html()

    return data_table

