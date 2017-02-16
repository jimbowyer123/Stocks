import stock_classes as sc
import stock_mini_functions as smf
import datetime
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
    # being held and the the cash value currently held
    def __init__(self):
        self.Trades=[]
        self.Quantity=0
        self.Value=0

    # Operation performed when a portfolio buys a stock
    def buy(self, buy_object):
        self.Trades.append(buy_object)
        self.Quantity+=buy_object.Quantity
        self.Value-= buy_object.Quantity * buy_object.Price

    # Operation performed when the portfolio sells stock
    def sell(self, sell_object):
        self.Trades.append(sell_object)
        self.Quantity-=1
        self.Value+=sell_object.Quantity*sell_object.Price

    # How the portfolio is viewed when printed
    def __repr__(self):
        return('Value=%2f Quantity=%d'%(self.Value,self.Quantity))

# Function for the first trading strategy which buys a stock when its close price
# goes from below the sma(30) to above the sma(30) and sells when the converse happens
def trade_strategy_one(symbol,start_date,end_date,portfolio=Portfolio()):
    # Retrieve the stock data over relevant period of time
    list_daily_bars=smf.read_daily_bars(symbol,start_date,end_date)

    # Create data series for opens, closes and the sma(30)of the closes
    open_series=sc.DataSeries(smf.get_list('Open',list_daily_bars),smf.get_list('Date',list_daily_bars))
    close_series=sc.DataSeries(smf.get_list('Close',list_daily_bars),smf.get_list('Date',list_daily_bars))
    sma_series=close_series.sma(30)

    # Start a loop which will run through the sma data series
    for i in range(1,len(sma_series.Dates)-1):
        # Starts a loop through the close series to find date corresponding to the sma date
        for j in range(len(close_series.Dates)):
            if sma_series.Dates[i]==close_series.Dates[j]:
                # Looks for case where stock price crosses the sma line from below to above
                if close_series.Data[j]>sma_series.Data[i] and close_series.Data[j-1]<sma_series.Data[i-1]:
                    # Buys a unit of the stock
                    buy_object=Buy_Object(open_series.Dates[j+1],open_series.Data[j+1])
                    portfolio.buy(buy_object)
                # Look for case where the stock price crosses the sma line from above to below
                if close_series.Data[j]<sma_series.Data[i] and close_series.Data[j-1]>sma_series.Data[i-1] and portfolio.Quantity>0:
                    # Sells a unit of the stock
                    sell_object=Sell_Object(open_series.Dates[j+1],open_series.Data[j+1])
                    portfolio.sell(sell_object)
    return(portfolio)

# Similar to the trade strategy above but using the ema(30) line instead of the sma(30)
def trade_strategy_two(symbol,start_date,end_date,portfolio=Portfolio()):
    list_daily_bars=smf.read_daily_bars(symbol,start_date,end_date)
    open_series=sc.DataSeries(smf.get_list('Open',list_daily_bars),smf.get_list('Date',list_daily_bars))
    close_series=sc.DataSeries(smf.get_list('Close',list_daily_bars),smf.get_list('Date',list_daily_bars))
    ema_series=close_series.ema(30)
    for i in range(1,len(ema_series.Dates)-1):
        now=ema_series.Dates[i]
        for \
                j in range(len(close_series.Dates)):
            if now==close_series.Dates[j]:
                if close_series.Data[j]>ema_series.Data[i] and close_series.Data[j-1]<ema_series.Data[i-1]:
                    buy_object=Buy_Object(open_series.Dates[j+1],open_series.Data[j+1])
                    portfolio.buy(buy_object)
                if close_series.Data[j]<ema_series.Data[i] and close_series.Data[j-1]>ema_series.Data[i-1] and portfolio.Quantity>0:
                    sell_object=Sell_Object(open_series.Dates[j+1],open_series.Data[j+1])
                    portfolio.sell(sell_object)
    return(portfolio)




