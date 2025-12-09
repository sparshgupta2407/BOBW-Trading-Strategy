import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Load tickers from CSV (assuming the file is named 'nse_Tickers.csv')
try:
    tickers_df = pd.read_csv('nse_tickers.csv')
    tickers = tickers_df.iloc[:, 0].tolist()  # Assuming tickers are in first column
except:
    # If CSV loading fails, use the hardcoded list you provided
    tickers = [
        '20MICRONS.NS', '21STCENMGM.NS', '360ONE.NS', '3IINFOLTD.NS',
        '3MINDIA.NS', '3PLAND.NS', '5PAISA.NS', '63MOONS.NS'
    ]

# Initialize results storage
results = []
yellow_dots_data = {
    'Ticker': [],
    'Yellow Dots': [],
    'Normalized_RS_Value': [],
    'Avg Dollar Volume': []
}

# Get market index data for RS calculation (Nifty 50)
nifty = yf.Ticker('^NSEI')
nifty_hist = nifty.history(period='1y')
mp = nifty_hist['Close'].iloc[-1]  # Current market price of index
mp1 = nifty_hist['Close'].iloc[0]   # Starting price of index for YTD

for ticker in tickers:
    try:
        # Try to get 1 year data first
        stock = yf.Ticker(ticker)
        data = stock.history(period='1y')
        
        # If we don't get enough data, try 3 months
        if len(data) < 200:
            data = stock.history(period='3mo')
            print(f"Using 3mo data for {ticker} (insufficient 1y data)")
            data['52W High'] = data['Close'].rolling(window=63).max()
            data['52W Low'] = data['Close'].rolling(window=63).min()
            data['150 SMA'] = data['Close'].rolling(window=63).mean()
            data['200 SMA'] = data['Close'].rolling(window=63).mean()
        else:
            data['52W High'] = data['Close'].rolling(window=252).max()
            data['52W Low'] = data['Close'].rolling(window=252).min()
            data['150 SMA'] = data['Close'].rolling(window=150).mean()
            data['200 SMA'] = data['Close'].rolling(window=200).mean()
        if len(data) == 0:
            print(f"No data available for {ticker}")
            continue
            
        # Calculate SMAs
        data['50 SMA'] = data['Close'].rolling(window=50).mean()
        
        
        # Calculate 52-week high/low
        data['52W High'] = data['Close'].rolling(window=252).max()
        data['52W Low'] = data['Close'].rolling(window=252).min()
        
        # Dollar Volume calculations
        data['Dollar Volume'] = data['Volume'] * data['Close']
        data['3M Avg Dollar Volume'] = data['Dollar Volume'].rolling(window=63).mean()
        
        # Check all conditions
        conditions_met = True
        
        # Condition 1: Last close above 150 and 200 SMA
        if not (data['Close'].iloc[-1] > data['150 SMA'].iloc[-1] and 
                data['Close'].iloc[-1] > data['200 SMA'].iloc[-1]):
            conditions_met = False
        
        # Condition 2: 150 DMA > 200 DMA
        if not (data['150 SMA'].iloc[-1] >= data['200 SMA'].iloc[-1]):
            conditions_met = False
            
        # Condition 3: 50 DMA > 150 DMA > 200 DMA
        if not (data['50 SMA'].iloc[-1] >= data['150 SMA'].iloc[-1] >= data['200 SMA'].iloc[-1]):
            conditions_met = False
            
        # Condition 4: Price relative to 52W range
        if not (data['Close'].iloc[-1] > data['52W Low'].iloc[-1] * 1.25 and
               data['Close'].iloc[-1] > data['52W High'].iloc[-1] * 0.75):
            conditions_met = False
            
        # Condition 5: 50 SMA trending up
        if len(data['50 SMA']) >= 2:
            if not (data['50 SMA'].iloc[-1] >= data['50 SMA'].iloc[-2]):
                conditions_met = False
        else:
            conditions_met = False
            
        # Condition 6: Close price relative to 50 SMA
        if not (data['Close'].iloc[-1] > data['50 SMA'].iloc[-1] * 0.93):
            conditions_met = False
            
        # Condition 7: 3M Avg Dollar Volume > 100M
        if len(data['3M Avg Dollar Volume'].dropna()) == 0 or data['3M Avg Dollar Volume'].iloc[-1] <= 100000000:
            conditions_met = False
            
        # Calculate Yellow Dots
        yellow_dots = 0
        for i in range(1, len(data)):
            if data['Volume'].iloc[i] > 1_000_000:
                price_change = (data['Close'].iloc[i] - data['Close'].iloc[i-1]) / data['Close'].iloc[i-1]
                if price_change > 0.05:
                    yellow_dots += 1
                elif price_change < -0.05:
                    yellow_dots -= 1
        
        # Calculate Normalized RS Value
        cm = data['Close'].iloc[-1]  # Current market price of stock
        cm1 = data['Close'].iloc[0]  # Starting price of stock for period
        normrs = ((cm / mp) * 100) / ((cm1 / mp1) * 100)
        
        # Calculate Avg Dollar Volume
        avg_dollar_volume = data['Dollar Volume'].mean()
        
        # Store yellow dots data
        yellow_dots_data['Ticker'].append(ticker)
        yellow_dots_data['Yellow Dots'].append(yellow_dots)
        yellow_dots_data['Normalized_RS_Value'].append(normrs)
        yellow_dots_data['Avg Dollar Volume'].append(avg_dollar_volume)
        
        if conditions_met:
            results.append(ticker)
            
    except Exception as e:
        print(f"Error processing {ticker}: {str(e)}")

# Create DataFrames from results
results_df = pd.DataFrame({'Tickers Meeting All Conditions': results})
yellow_dots_df = pd.DataFrame(yellow_dots_data)

# Display results
print("\nStocks meeting all conditions:")
print(results_df)
print("\nYellow Dots Analysis:")
print(yellow_dots_df)
