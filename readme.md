# 📈 BOBW Trading Strategy 
*A Python-based Technical Screening System for High-Probability Breakouts*

This repository contains a high-performance stock screening script built using **Python**, **Pandas**, and **Yahoo Finance (yfinance)**.  
The screener evaluates NSE-listed stocks based on **trend strength**, **volume analysis**, **relative strength**, and **moving average alignment** — helping identify stocks with strong institutional accumulation and breakout potential.

---

## 🚀 Features

### ✔️ 1. Automatic Ticker Loading
- Loads tickers from `nse_tickers.csv`
- Falls back to a predefined list if the file is missing

### ✔️ 2. Smart Data Downloading
- Downloads **1-year data** by default  
- Automatically switches to **3-month data** if insufficient candles are available

### ✔️ 3. Technical Indicators Computed
- 50 SMA  
- 150 SMA  
- 200 SMA  
- 52-Week High  
- 52-Week Low  
- Dollar Volume  
- 3-Month Avg Dollar Volume  
- Normalized Relative Strength (vs NIFTY)  
- Yellow Dots (Volume + Price Spike Detection)

### ✔️ 4. Seven Strict Screening Conditions
A stock passes only if it satisfies all:

1. Price > 150 SMA and 200 SMA  
2. 150 SMA > 200 SMA  
3. 50 SMA > 150 SMA > 200 SMA  
4. Price must be in the correct 52-week range  
5. 50 SMA must be trending up  
6. Price must be at least 93% of 50 SMA  
7. 3-month Avg Dollar Volume > ₹100,000,000  

### ✔️ 5. Yellow Dots Indicator
A custom volume-spike detector:

- +1 for a bullish spike on >1M volume  
- –1 for a bearish collapse on >1M volume  

Useful for identifying institutional footprints.

---

# 🏆 Real-World Performance of Picks

Below are actual returns generated using this screener:

| Stock | Return | Days |
|-------|--------|-------|
| Muthoot | **28%** | 16 days |
| NH | **35%** | 18 days |
| SBICARD | **12%** | 5 days |
| LloydsME | **14%** | 3 days |
| BEL | **14.5%** | 14 days |
| Force Motors | **44%** | 20 days |
| Laurus Labs | **25%** | 18 days |
| Cosmo First | **18%** | 13 days |
| ITD Cementation | **21%** | 7 days |
| Maharashtra Seamless | **12%** | 3 days |
| MCX | **24%** | 15 days |
| Reliance Infrastructure | **16%** | 4 days |
| CUB | **24%** | 8 days |
| Affle | **10%** | 9 days |
| TFCI | **20%** | 7 days |
| Reddington | **15%** | 7 days |
| Sharda Cropchem | **42%** | 25 days |
| GRM Overseas | **10%** | 14 days |
| RBL Bank | **10%** | 10 days |
| ABDL | **20%** | 13 days |
| 63Moons | **15%** | 2 days |

These results highlight the system’s ability to capture strong relative strength and trend-driven breakout candidates.

---

## 🔧 How to Run

### 1. Install dependencies
```bash
pip install yfinance pandas
