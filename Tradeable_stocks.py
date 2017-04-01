# Run this program to get you a list of stocks
# that we can get the trade info for

import shelve
import finsymbols
import stock_mini_functions as smf
import _datetime


# Open a file to store the information in
shelve_stock_evo_data = shelve.open('shelve_stock_evo_data')
# Create the list for tradeable stocks
tradeable_stocks=[]
# Get lists of stocks data from nasdaq, nyse and amex
nasdaq=finsymbols.get_nasdaq_symbols()
nyse=finsymbols.get_nyse_symbols()
amex=finsymbols.get_amex_symbols()
# Create a list of symbols from nasdaq, nyse and amex
all_nasdaq_symbols=[]
for n in range(len(nasdaq)):
    all_nasdaq_symbols.append(nasdaq[n]['symbol'])
all_nyse_symbols=[]
for n in range(len(nyse)):
    all_nyse_symbols.append(nyse[n]['symbol'])
all_amex_symbols=[]
for n in range(len(amex)):
    all_amex_symbols.append(amex[n]['symbol'])
# Try to find the symbols that we can test on
for symbol in all_nasdaq_symbols:
    # Try to retrieve data and if we can than add it to the tradeable stocks list
    try:
        smf.read_daily_bars(symbol)
        tradeable_stocks.append(symbol)
    except Exception:
        pass
for symbol in all_nyse_symbols:
    # Same as above but making sure we don't add the same symbols multiple times
    if symbol not in tradeable_stocks:
        try:
            smf.read_daily_bars(symbol)
            tradeable_stocks.append(symbol)
        except Exception:
            pass
for symbol in all_amex_symbols:
   # Same as above
   if symbol not in tradeable_stocks:
        try:
            smf.read_daily_bars(symbol)
            tradeable_stocks.append(symbol)
        except Exception:
            pass
# Save the updated list of tradeable stocks in a shelve file
shelve_stock_evo_data['tradeable_stocks']=tradeable_stocks

print('done')