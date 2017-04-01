import stock_plots as sp
import datetime
import first_stock_functions as fsf
import Trading_Strategy as TS
import Evolution_Classes as EC
import YahooTickerDownloader as YTD
import finsymbols
import stock_mini_functions as smf
import pickle
import random
import shelve

#today = datetime.date.today()
#last_year = today - datetime.timedelta(days=365)
#sp.plot_candlestick_with_sma_ema('CPAAW',last_year,today,30)
#print(fsf.analyse_recent_year('AAPL'))
#u=2
#try:
#    smf.read_daily_bars('human',last_year,today)
#    u=4
#except Exception:
#    pass
#TS.Portfolio().trade_strategy_one('DWA',last_year,today,30)
#TS.Portfolio().trade_strategy_crossed_sma_with_constant_trade_cost('RL',last_year,today,30,100)
#test_population= EC.Population([],['Chrome_1','Chrome_2'])
#for i in range(50):
#    chrome_1=EC.Chromosome('Chrome_1',range(6),random.randint(0,5))
#    chrome_2=EC.Chromosome('Chrome_2',range(50),random.randint(0,49))
#    new_person=EC.Person([chrome_1,chrome_2],random.randint(1,100))
#    test_population.People.append(new_person)
#test_population.kill()
#test_population.mutate(0.5)
#TS.run_sma_ema_evolution(0.1,100)
#nyse=finsymbols.get_nyse_symbols()
shelve_stock_evo_data = shelve.open('shelve_stock_evo_data')
population=shelve_stock_evo_data['sma_ema_final_population']
#amex=finsymbols.get_amex_symbols()
#tradeable_stocks=shelve_stock_evo_data['tradeable_stocks']
print('done')