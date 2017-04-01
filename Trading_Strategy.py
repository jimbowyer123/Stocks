import stock_classes as sc
import stock_mini_functions as smf
import datetime
import Evolution_Classes as EC
import random
import finsymbols
import shelve
# Create basic class for the buy trade of a stock
class Buy_Object:
    # Buy_Object will contain date of transaction, price of the transaction per unit
    # and how many units were bought
    def __init__(self, date, price, quantity=1):
        self.Date=date
        self.Price=price
        self.Quantity=quantity

    # Simply shows how to represent the buy object when displayed
    def __repr__(self):
        date=smf.timestamp_to_datetime([self.Date])
        year=date[0].year
        month=date[0].month
        day=date[0].day
        return('<Buy: Date=%d/%d/%d,Price=%0.2f, Quantity=%d>'%(year,month,day,self.Price,self.Quantity))

# Creating basic class for the selling of an object
# Follows very similar to the buy object just with selling instead
class Sell_Object:
    def __init__(self,date,price,quantity=1):
        self.Date=date
        self.Price=price
        self.Quantity=quantity
    def __repr__(self):
        date=smf.timestamp_to_datetime([self.Date])
        year=date[0].year
        month=date[0].month
        day=date[0].day
        return('<Sell: Date=%d/%d/%d,Price=%0.2f, Quantity=%d>'%(year,month,day,self.Price,self.Quantity))

# Creating a class for portfolios which are the objects that will get run
# through the different trading strategies
class Portfolio:
    # Will contain the list of tades performed, how much stock is currently
    # being held and the the cash value currently held along with the total value
    # of the Portfolio
    def __init__(self):
        self.Trades=[]
        self.Quantity=0
        self.Capital=0
        self.Value=0

    # Operation performed when a portfolio buys a stock
    def buy(self, buy_object):
        self.Trades.append(buy_object)
        self.Quantity+=buy_object.Quantity
        self.Capital-= buy_object.Quantity * buy_object.Price

    # Operation performed when the portfolio sells stock
    def sell(self, sell_object):
        self.Trades.append(sell_object)
        self.Quantity-=sell_object.Quantity
        self.Capital+= sell_object.Quantity * sell_object.Price

    # Function for the first trading strategy which buys a stock when its close price
    # goes from below the sma(30) to above the sma(30) and sells when the converse happens
    def trade_strategy_one(self,symbol, start_date, end_date, sma_length,):
        # Retrieve the stock data over relevant period of time
        list_daily_bars = smf.read_daily_bars(symbol, start_date, end_date)

        # Create data series for opens, closes and the sma(30)of the closes
        open_series = sc.DataSeries(smf.get_list('Open', list_daily_bars), smf.get_list('Date', list_daily_bars))
        close_series = sc.DataSeries(smf.get_list('Close', list_daily_bars), smf.get_list('Date', list_daily_bars))
        sma_series = close_series.sma(sma_length)

        # Start a loop which will run through the sma data series
        for i in range(1, len(sma_series.Dates) - 1):
            # Starts a loop through the close series to find date corresponding to the sma date
            for j in range(len(close_series.Dates)):
                if sma_series.Dates[i] == close_series.Dates[j]:
                    # Looks for case where stock price crosses the sma line from below to above
                    if close_series.Data[j] > sma_series.Data[i] and close_series.Data[j - 1] < sma_series.Data[i - 1]:
                        # Buys a unit of the stock
                        buy_object = Buy_Object(open_series.Dates[j + 1], open_series.Data[j + 1])
                        self.buy(buy_object)
                        print(buy_object)
                    # Look for case where the stock price crosses the sma line from above to below
                    if close_series.Data[j] < sma_series.Data[i] and close_series.Data[j - 1] > sma_series.Data[i - 1] and self.Quantity > 0:
                        # Sells a unit of the stock
                        sell_object = Sell_Object(open_series.Dates[j + 1], open_series.Data[j + 1])
                        self.sell(sell_object)
                        print(sell_object)
        print('Total profit = ' + str(self.Capital + self.Quantity * close_series.Data[-1]))
        return (self)

    # Similar to the trade strategy above but using the ema(30) line instead of the sma(30)
    def trade_strategy_two(self,symbol, start_date, end_date, ema_length):
        list_daily_bars = smf.read_daily_bars(symbol, start_date, end_date)
        open_series = sc.DataSeries(smf.get_list('Open', list_daily_bars), smf.get_list('Date', list_daily_bars))
        close_series = sc.DataSeries(smf.get_list('Close', list_daily_bars), smf.get_list('Date', list_daily_bars))
        ema_series = close_series.ema(ema_length)
        for i in range(1, len(ema_series.Dates) - 1):
            now = ema_series.Dates[i]
            for j in range(len(close_series.Dates)):
                if now == close_series.Dates[j]:
                    if close_series.Data[j] > ema_series.Data[i] and close_series.Data[j - 1] < ema_series.Data[i - 1]:
                        buy_object = Buy_Object(open_series.Dates[j + 1], open_series.Data[j + 1])
                        self.buy(buy_object)
                        print(buy_object)
                    if close_series.Data[j] < ema_series.Data[i] and close_series.Data[j - 1] > ema_series.Data[
                                i - 1] and self.Quantity > 0:
                        sell_object = Sell_Object(open_series.Dates[j + 1], open_series.Data[j + 1])
                        self.sell(sell_object)
                        print(sell_object)
        print('Total profit = ' + str(self.Capital + self.Quantity * close_series.Data[-1]))
        return (self)


    # Trying to create a similar sma trade strategy but with given costs of each trade
    def trade_strategy_crossed_sma_with_constant_trade_cost(self,symbol,start_date,end_date,sma_length,trade_value):
        # Retrieve the stock data over relevant period of time
        list_daily_bars = smf.read_daily_bars(symbol, start_date, end_date)

        # Create data series for opens, closes and the sma(30)of the closes
        open_series = sc.DataSeries(smf.get_list('Open', list_daily_bars), smf.get_list('Date', list_daily_bars))
        close_series = sc.DataSeries(smf.get_list('Close', list_daily_bars), smf.get_list('Date', list_daily_bars))
        sma_series = close_series.sma(sma_length)

        # Crete a loop that spans the length of the sma dates list excluding the first date
        # as we can't tell if the line iis crossed for the first date (need to think about
        # whether we actually can include this
        for i in range(1, len(sma_series.Dates) - 1):
            # Now a loop running through the close price dates so we can equate the sma date
            # and the close date.
            for j in range(len(close_series.Dates)):
                # Choose elements such that the dates match
                if sma_series.Dates[i] == close_series.Dates[j]:
                    # Check to see if the sma line has been crossed by the stock price going up
                    if close_series.Data[j] > sma_series.Data[i] and close_series.Data[j - 1] < sma_series.Data[i - 1]:
                        # Will need to find the number of units to buy that gets the cost closest to £100
                        # then buy this amount of stock
                        n=0
                        price=open_series.Data[j+1]
                        while n*price<trade_value:
                            n=n+1
                        buy_object=Buy_Object(open_series.Dates[j+1],price,n-1)
                        self.buy(buy_object)

                    # Check to see if the sma line has been crossed by the stock price going down
                    if close_series.Data[j]<sma_series.Data[i] and close_series.Data[j-1]>sma_series.Data[i-1] and self.Quantity>0:
                        # Sell the stock we hold
                        sell_object=Sell_Object(open_series.Dates[j+1],open_series.Data[j+1],self.Quantity)
                        self.sell(sell_object)
        # Update the total Value of the Portfolio
        self.Value=self.Capital + self.Quantity*close_series.Data[-1]
        return(self)

    # Trying to create a similar ema trade strategy but with given costs of each trade
    # The code is very similar to the sma one so look at that for explanation of what is
    # happening
    def trade_strategy_crossed_ema_with_constant_trade_cost(self, symbol, start_date, end_date, ema_length, trade_value):
        # Retrieve the stock data over relevant period of time
        list_daily_bars = smf.read_daily_bars(symbol, start_date, end_date)

        # Create data series for opens, closes and the ema(30)of the closes
        open_series = sc.DataSeries(smf.get_list('Open', list_daily_bars), smf.get_list('Date', list_daily_bars))
        close_series = sc.DataSeries(smf.get_list('Close', list_daily_bars), smf.get_list('Date', list_daily_bars))
        ema_series = close_series.ema(ema_length)

        for i in range(1, len(ema_series.Dates) - 1):
            for j in range(len(close_series.Dates)):
                if ema_series.Dates[i] == close_series.Dates[j]:
                    if close_series.Data[j] > ema_series.Data[i] and close_series.Data[j - 1] < ema_series.Data[i - 1]:
                        # Will need to find the number of units to buy that gets the cost closest to £100
                        n = 0
                        price = open_series.Data[j + 1]
                        while n * price < trade_value:
                            n = n + 1
                        buy_object = Buy_Object(open_series.Dates[j + 1], price, n - 1)
                        self.buy(buy_object)

                    if close_series.Data[j] < ema_series.Data[i] and close_series.Data[j - 1] > ema_series.Data[i - 1] and self.Quantity > 0:
                        sell_object = Sell_Object(open_series.Dates[j + 1], open_series.Data[j + 1], self.Quantity)
                        self.sell(sell_object)
        self.Value = self.Capital + self.Quantity * close_series.Data[-1]
        return (self)

    def trade_from_daily_bars_ema_constant_trade_cost(self,list_daily_bars,ema_length,trade_value):
        # Create data series for opens, closes and the ema(30)of the closes
        open_series = sc.DataSeries(smf.get_list('Open', list_daily_bars), smf.get_list('Date', list_daily_bars))
        close_series = sc.DataSeries(smf.get_list('Close', list_daily_bars), smf.get_list('Date', list_daily_bars))
        ema_series = close_series.ema(ema_length)

        for i in range(1, len(ema_series.Dates) - 1):
            for j in range(len(close_series.Dates)):
                if ema_series.Dates[i] == close_series.Dates[j]:
                    # Is the share price crossing from below to above
                    if close_series.Data[j] > ema_series.Data[i] and close_series.Data[j - 1] < ema_series.Data[i - 1]:
                        # Will need to find the number of units to buy that gets the cost closest to £100
                        n = 0
                        price = open_series.Data[j + 1]
                        while n * price < trade_value:
                            n = n + 1
                        # Apply the buy to the Portfolio
                        buy_object = Buy_Object(open_series.Dates[j + 1], price, n - 1)
                        self.buy(buy_object)

                    # Is the share price crossing from above to below
                    if close_series.Data[j]<ema_series.Data[i] and close_series.Data[j-1]>ema_series.Data[i-1] and self.Quantity>0:
                        # Sell all the shares you currently have of the stock
                        sell_object = Sell_Object(open_series.Dates[j + 1], open_series.Data[j + 1], self.Quantity)
                        self.sell(sell_object)
        # Update the value of the Portfolio
        self.Value = self.Capital + self.Quantity * close_series.Data[-1]
        return (self)

    def trade_from_daily_bars_sma_constant_trade_cost(self,list_daily_bars,sma_length,trade_value):
        # Create data series for opens, closes and the sma(30)of the closes
        open_series = sc.DataSeries(smf.get_list('Open', list_daily_bars), smf.get_list('Date', list_daily_bars))
        close_series = sc.DataSeries(smf.get_list('Close', list_daily_bars), smf.get_list('Date', list_daily_bars))
        sma_series = close_series.sma(sma_length)

        # Create a loop that spans the length of the sma dates list excluding the first date
        # as we can't tell if the line iis crossed for the first date (need to think about
        # whether we actually can include this
        for i in range(1, len(sma_series.Dates) - 1):
            # Now a loop running through the close price dates so we can equate the sma date
            # and the close date.
            for j in range(len(close_series.Dates)):
                # Choose elements such that the dates match
                if sma_series.Dates[i] == close_series.Dates[j]:
                    # Check to see if the sma line has been crossed by the stock price going up
                    if close_series.Data[j] > sma_series.Data[i] and close_series.Data[j - 1] < sma_series.Data[i - 1]:
                        # Will need to find the number of units to buy that gets the cost closest to £100
                        # then buy this amount of stock
                        n = 0
                        price = open_series.Data[j + 1]
                        while n * price < trade_value:
                            n = n + 1
                        buy_object = Buy_Object(open_series.Dates[j + 1], price, n - 1)
                        self.buy(buy_object)

                    # Check to see if the sma line has been crossed by the stock price going down
                    if close_series.Data[j] < sma_series.Data[i] and close_series.Data[j - 1] > sma_series.Data[
                                i - 1] and self.Quantity > 0:
                        # Sell the stock we hold
                        sell_object = Sell_Object(open_series.Dates[j + 1], open_series.Data[j + 1], self.Quantity)
                        self.sell(sell_object)
        # Update the total Value of the Portfolio
        self.Value = self.Capital + self.Quantity * close_series.Data[-1]
        return (self)



    # Want a function that can print the trades of a Portfolio
    def print_trades(self):
        for trade in self.Trades:
            print(trade)

    # How the portfolio is viewed when printed
    def __repr__(self):
        return ('Capital=%2f Quantity=%d Value=%2f' % (self.Capital, self.Quantity, self.Value))

# Crete a class that has the characteristics of our chosen strategy
class Portfolio_Strategy_SMA_EMA:
    def __init__(self,ema_indicator,ema_number,sma_indicator,sma_number,trade_value=100):
        # Indicator tells us if it will trade using the ema/sma
        self.EMA_Indicator=ema_indicator
        # Number tells us what length ema/sma we are using
        self.EMA_Number=ema_number
        self.SMA_Indicator=sma_indicator
        self.SMA_Number=sma_number
        # Give the strategy a defining portfolio
        self.Value=0
        # Since I will be applying the constant trade value functions this value is a characteristic
        self.Trade_Value=trade_value

    # Function that allows us to apply our strategy to a certain list of stocks
    def trade_on(self,list_of_daily_bars_lists,start_date=datetime.datetime.today()-datetime.timedelta(days=365),end_date=datetime.datetime.today()):
        # Run through the different tickers so that we can apply trades on each one
        for list_daily_bars in list_of_daily_bars_lists:
            # Check to see if we are running an ema trading strategy
            if self.EMA_Indicator == 1:
                # Create a dummy Portfolio
                Test_Portfolio=Portfolio()
                # Run ema strategy on dummy portfolio with characteristics of this Portfolio Strategy
                Test_Portfolio.trade_from_daily_bars_ema_constant_trade_cost(list_daily_bars,self.EMA_Number,self.Trade_Value)
                # Update the value of the Portfolio Strategy
                self.Value += Test_Portfolio.Value

            # Check to see if we are running the sma trading strategy
            if self.SMA_Indicator == 1:
                # Create a dummy portfolio
                Test_Portfolio=Portfolio()
                # Run sma strategy on dummy portfolio with characteristics of this Portfolio Strategy
                Test_Portfolio.trade_from_daily_bars_sma_constant_trade_cost(list_daily_bars,self.SMA_Number,self.Trade_Value)
                # Update the value of the Portfolio strategy
                self.Value += Test_Portfolio.Value




# Start on the function to run an evolution algorithm on sma/ema strategies
def run_sma_ema_evolution(mutation_coefficient,generations):
    shelve_stock_evo_data=shelve.open('shelve_stock_evo_data')
    # Will collect a list of stock symbols
    tradeable_stocks=shelve_stock_evo_data['tradeable_stocks']
    # We need to create the relevant population for this strategy
    Strategy_Population=EC.Population([],('EMA_Indicator','EMA_Number','SMA_Indicator','SMA_Number'))
    # Want 50 people in the population
    for i in range(50):
        EMA_Indicator=EC.Chromosome('EMA_Indicator',(0,1),random.randint(0,1))
        SMA_Indicator=EC.Chromosome('SMA_Indicator',(0,1),random.randint(0,1))
        EMA_Number=EC.Chromosome('EMA_Number',range(2,100),random.randint(2,99))
        SMA_Number=EC.Chromosome('SMA_Number', range(2, 100), random.randint(2, 99))
        Strategy=EC.Person((EMA_Indicator,EMA_Number,SMA_Indicator,SMA_Number),0)
        Strategy_Population.People.append(Strategy)
    # Need to create the scores for the population
    # First it needs to have some test symbols to run
    test_daily_bars=[]
    while len(test_daily_bars)<10:
        try:
            symbol=tradeable_stocks[random.randint(0,len(tradeable_stocks)-1)]
            list_daily_bars=smf.read_daily_bars(symbol)
            test_daily_bars.append(list_daily_bars)

        except Exception:
            pass
    for Person in Strategy_Population.People:
        # Create a portfolio strategy sma ema class with relevant inputs
        Port_Strat_Initial=Portfolio_Strategy_SMA_EMA(Person.Chromosomes[0].Value,Person.Chromosomes[1].Value,Person.Chromosomes[2].Value,Person.Chromosomes[3].Value)
        # Apply the relevant trades on the stock
        Port_Strat_Initial.trade_on(test_daily_bars)
        # Let the score for a person be the value of the corresponding Portfolio
        Person.Score=Port_Strat_Initial.Value
    # Check we aren't at teh generation limit for the population
    while Strategy_Population.Generation<generations:
        # Kill of the lower scoring people of the population
        Strategy_Population.kill()
        # Mutate the remaining members of the population
        Strategy_Population.mutate(mutation_coefficient)
        # Create a new list of tradeable stocks data to run this iteration on
        test_daily_bars=[]
        while len(test_daily_bars)<10:
            try:
                symbol = tradeable_stocks[random.randint(0, len(tradeable_stocks) - 1)]
                list_daily_bars=smf.read_daily_bars(symbol)
                test_daily_bars.append(list_daily_bars)
            except Exception:
                pass
        # Run another iteration test on the new population
        for Person in Strategy_Population.People:
            # Create Strategy to represent a person
            Port_Strat=Portfolio_Strategy_SMA_EMA(Person.Chromosomes[0].Value,Person.Chromosomes[1].Value,Person.Chromosomes[2].Value,Person.Chromosomes[3].Value)
            # Trade on the test data
            Port_Strat.trade_on(test_daily_bars)
            # Update the score of the person
            Person.Score=Port_Strat.Value
    # Save the population into shelve file
    shelve_stock_evo_data['sma_ema_final_population']=Strategy_Population
    shelve_stock_evo_data.close()
    return(Strategy_Population)
