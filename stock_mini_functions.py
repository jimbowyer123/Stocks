import datetime
import pandas_datareader.data as web
import stock_classes as sc
from statistics import mean

# Function that produces a list of Bars for a stock from a start date to an end date
def read_daily_bars(symbol_ticker,start_date,end_date):
    df=web.DataReader(symbol_ticker,'yahoo',start_date,end_date)
    list_daily_bars=[]
    for i in range(len(df)):
        list_daily_bars.append(sc.Daily_Bar(df['Open'][i],df['High'][i],df['Low'][i],df['Close'][i],df.index[i],df['Volume'][i]))
    return (list_daily_bars)

# Need Function to return a list of specific values from a list of daily bars
def get_list(value, KeyFigures):
    list=[]
    for i in range(len(KeyFigures)):
        list.append(KeyFigures[i].__getattribute__(value))
    return(list)

# Need to write a function that coverts a list of pandas TimeStamp dates to datetime objects
def timestamp_to_datetime(list_timestamp):
    list_datetime=[]
    for i in range(len(list_timestamp)):
        list_datetime.append(list_timestamp[i].to_pydatetime())
    return(list_datetime)

# Function that converts a datetime object to a string
def make_string_date(date):
    return(str(date.year) + '-' + str(date.month) + '-' + str(date.day))


# Start the overall purpose function which returns the years OHLC, average
# OHLC and company name for a given symbol
def analyse_recent_year(symbol):
    # Find the date today as datetime object
    today = datetime.date.today()

    # Create date time object for last year
    last_year = today - datetime.timedelta(days=365)

    # Create a list of daily bars for given symbol over given period of time
    list_daily_bars=read_daily_bars(symbol,last_year,today)

    # Retrieve the OHLC of the stock for each day of the year
    list_opens=get_list('Open', list_daily_bars)
    list_close=get_list('Close', list_daily_bars)
    list_highs=get_list('High', list_daily_bars)
    list_lows=get_list('Low', list_daily_bars)
    list_volumes=get_list('Volume',list_daily_bars)

    # Extract the OHLC for the years period
    year_open=list_opens[0]
    year_close=list_close[-1]
    year_high=max(list_highs)
    year_low=min(list_lows)
    year_volume=sum(list_volumes)
    # Calculate the Average OHLC for the years period
    average_open=mean(list_opens)
    average_close=mean(list_close)
    average_high=mean(list_highs)
    average_low=mean(list_lows)
    average_volume=mean(list_volumes)

    # Answer a tuple, the first element is the OHLC bar for the year and the second element is the
    # average bar for the year. The third element is the share name. Tuples are nice ways to return more than one thing from a function.
    return((sc.Bar(year_open,year_high,year_low,year_close,year_volume),sc.Bar(average_open,average_high,average_low,average_close,average_volume),symbol))
