import stock_plots as sp
import datetime
import first_stock_functions as fsf
import Trading_Strategy as TS
import Evolution_Classes as EC
import random

#today = datetime.date.today()
#last_year = today - datetime.timedelta(days=365)

#sp.plot_candlestick_with_sma_ema('RL',last_year,today,30)
#print(fsf.analyse_recent_year('AAPL'))

#TS.Portfolio().trade_strategy_one('DWA',last_year,today,30)
#TS.Portfolio().trade_strategy_crossed_sma_with_constant_trade_cost('RL',last_year,today,30,100)
people=[]
for i in range(50):
    people.append(EC.Person([],[],random.randint(1,500)))

Test_Population=EC.Population(people,[])

New_Test_Population=Test_Population.kill()
