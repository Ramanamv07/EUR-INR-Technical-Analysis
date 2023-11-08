import requests
from bs4 import BeautifulSoup
import pandas as pd

# Scrape Currency Data
stock_symbol = 'EURINR%3DX'

# Yahoo Finance URL for historical data
url = f'https://finance.yahoo.com/quote/{stock_symbol}/history?period1=1667869091&period2=1699405091&interval=1d&events=history&includeAdjustedClose=true'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Send an HTTP GET request
response = requests.get(url, headers=headers)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the historical data table
table = soup.find('table', {'data-test': 'historical-prices'})

# Extract historical data
historical_data = []

if table:
    rows = table.find_all('tr')
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) == 7:  # Ensure it's a data row
            date = cols[0].get_text()
            open_price = cols[1].get_text()
            high_price = cols[2].get_text()
            low_price = cols[3].get_text()
            close_price = cols[4].get_text()
            adj_close_price = cols[5].get_text()
            volume = cols[6].get_text()

            historical_data.append({
                'Date': date,
                'Open': open_price,
                'High': high_price,
                'Low': low_price,
                'Close': close_price,
                'Adj Close': adj_close_price,
                'Volume': volume
            })

print (historical_data)