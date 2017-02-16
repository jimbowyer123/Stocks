import stock_plots as sp
import datetime
import first_stock_functions as fsf
import Trading_Strategy as TS


today = datetime.date.today()
last_year = today - datetime.timedelta(days=365)

sp.plot_candlestick_with_sma_ema('RL',last_year,today,30)
#print(fsf.analyse_recent_year('AAPL'))
x=TS.trade_strategy_one('RL',last_year,today)
y=TS.trade_strategy_two('RL',last_year,today)
print(x)
print(x.Trades)
print(y)
print(y.Trades)
