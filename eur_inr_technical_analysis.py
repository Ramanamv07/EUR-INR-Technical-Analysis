import yfinance as yf
import pandas as pd

# Define the currency pair and date range
currency_pair = 'EURINR=X'
start_date = '2023-01-01'
end_date = '2023-11-03' # End date is November 3 because it only extracts data upto previous day(Nov 2)

# Step 1: Scrape Currency Data using yfinance
currency_data = yf.download(currency_pair, start=start_date, end=end_date)

# Step 2: Technical analysis for upcoming day
def calculate_technical_indicators_1d(currency_data):
    df = currency_data.copy()
    ti = {}

    # Calculate 10-day simple moving average (SMA)
    data = df.loc["2023-10-24":"2023-11-02"]
    ti['SMA'] = data['Close'].mean()

    # Calculate Bollinger Bands for 20 days
    data = df.loc["2023-10-14":"2023-11-02"]
    ti['SMA_20'] = data['Close'].mean()
    ti['STD'] = data['Close'].std()
    ti['Upper_band'] = ti['SMA_20'] + (2 * ti['STD'])
    ti['Lower_band'] = ti['SMA_20'] - (2 * ti['STD'])

    # Calculate CCI (Commodity Channel Index) for 14 days period
    data = df.loc["2023-10-20":"2023-11-02"]

    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    l = len(typical_price)-1
    tp = typical_price.iloc[l]
    sma = typical_price.mean()
    mean_deviation = (typical_price - sma).abs().mean()
    cci = (tp - sma) / (0.015 * mean_deviation)
    ti['CCI'] = cci

    return ti

day_ti = calculate_technical_indicators_1d(currency_data)

# Step 3: Technical analysis for upcoming week
def calculate_technical_indicators_1w(currency_data):
    df = currency_data.copy()
    ti = {}

    # Calculate simple moving average (SMA)
    data = df.loc["2023-08-25":"2023-11-02"]
    ti['SMA'] = data['Close'].mean()

    # Calculate Bollinger Bands
    data = df.loc["2023-06-16":"2023-11-02"]
    ti['SMA_'] = data['Close'].mean()
    ti['STD'] = data['Close'].std()
    ti['Upper_band'] = ti['SMA_'] + (2 * ti['STD'])
    ti['Lower_band'] = ti['SMA_'] - (2 * ti['STD'])

    # Calculate CCI (Commodity Channel Index)
    data = df.loc["2023-07-28":"2023-11-02"]

    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    l = len(typical_price)-1
    tp = typical_price.iloc[l]
    sma = typical_price.mean()
    mean_deviation = (typical_price - sma).abs().mean()
    cci = (tp - sma) / (0.015 * mean_deviation)
    ti['CCI'] = cci

    return ti

week_ti = calculate_technical_indicators_1w(currency_data)

# Step 4: Make a decision
def make_decision(ma, upper_band, lower_band, cci):
    if ma > upper_band and cci > 100:
        return "SELL"
    elif ma < lower_band and cci < -100:
        return "BUY"
    else:
        return "NEUTRAL"

decision_one_day = make_decision(day_ti['SMA'], day_ti['Upper_band'], day_ti['Lower_band'], day_ti['CCI'])
decision_one_week = make_decision(week_ti['SMA'], week_ti['Upper_band'], week_ti['Lower_band'], week_ti['CCI'])

# Step 5: Output
print("\n\n\t\tTrading Decision for Upcoming Day")
print("\n\tMoving Average:", day_ti['SMA'])
print("\tUpper Band of Ballinger band:", day_ti['Upper_band'])
print("\tLower Band of Ballinger band:", day_ti['Lower_band'])
print("\tCCI(Commodity Channel Index):", day_ti['CCI'])
print("\n\tFinal Trading Decision for Upcoming Day:", decision_one_day)

print("\n\n\t\tTrading Decision for Upcoming Week")
print("\n\tMoving Average:", week_ti['SMA'])
print("\tUpper Band of Ballinger band:", week_ti['Upper_band'])
print("\tLower Band of Ballinger band:", week_ti['Lower_band'])
print("\tCCI(Commodity Channel Index):", week_ti['CCI'])
print("\n\tFinal Trading Decision for Upcoming Week:", decision_one_week)
print("\n\n")