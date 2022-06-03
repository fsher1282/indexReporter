import yfinance as yf


class IndexCollector:
    """
    Index collector uses yfinance library to get important information on indexes/stocks/bonds etc.
    that would be relavent on a week by week basis then returns them as a dictionary

    """

    def __init__(self, tickers):
        # Initialize list of all values to be gathered
        self.tickers = tickers
        self.current_prices = []
        self.prev_closes = []
        self.last_weeks_closes = []
        self.daily_changes = []
        self.weekly_changes = []
        self.long_names = []

    @staticmethod
    def get_current_price(tick):
        # Get today's price
        today_data = yf.Ticker.history(tick, period='1d')
        return round(today_data['Close'][0], 2)

    @staticmethod
    def get_last_weeks_close(tick):
        # Get last week's closing price
        today_data = yf.Ticker.history(tick, period='6d')
        return round(today_data['Close'][0], 2)

    def collect_data(self):
        # Loop through each ticker to get values and organize in dictionary
        for tick in self.tickers:
            ticker = yf.Ticker(tick)

            # Collect scraped values
            current_price = round(self.get_current_price(ticker), 2)
            prev_close = round(ticker.info['previousClose'], 2)
            last_weeks_close = round(self.get_last_weeks_close(ticker), 2)

            # Infer other values based off scrapped values
            daily_change = round(current_price - prev_close, 2)
            weekly_change = round(current_price - last_weeks_close, 2)

            # Remove trailing decimal points
            current_price = "{:,.2f}".format(current_price)
            prev_close = "{:,.2f}".format(prev_close)
            last_weeks_close = "{:,.2f}".format(last_weeks_close)
            daily_change = "{:,.2f}".format(daily_change)
            weekly_change = "{:,.2f}".format(weekly_change)

            # Append scrapped data to ordered lists
            self.long_names.append(str(ticker.info['shortName']))
            self.current_prices.append(str(current_price))
            self.prev_closes.append(str(prev_close))
            self.last_weeks_closes.append(str(last_weeks_close))
            self.daily_changes.append(str(daily_change))
            self.weekly_changes.append(str(weekly_change))

        # Store collected data in a dictionary
        data_table = {'Index': self.long_names,
                      "Current Prices": self.current_prices,
                      'Prev.Close': self.prev_closes,
                      "Today's Change": self.daily_changes,
                      'L.W Change': self.last_weeks_closes,
                      '1-Week Change': self.weekly_changes}

        return data_table

    def __del__(self):
        print('IndexCollector has been deleted...')
