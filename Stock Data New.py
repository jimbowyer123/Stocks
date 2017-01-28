import pandas_datareader.data as web
from datetime import datetime
import datetime
from statistics import mean
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
# Create a class to contain relevant stock values for a time period
class Bar:
    def __init__(self,open,high,low,close,volume):
        self.Open=open
        self.High=high
        self.Low=low
        self.Close=close
        self.Volume=volume
    def __repr__(self):
        return('O=%0.2f, H=%0.2f, L=%0.2f, C=%0.2f, V=%d'%(self.Open,self.High,self.Low,self.Close,self.Volume))

# Also want a daily Bar that contain the OHLC of a stock with the date and stock symbol
class Daily_Bar(Bar):
    def __init__(self, open, high, low, close,date,volume):
        super().__init__(open,high,low,close,volume)
        self.Date=date

class DataSeries:
    def __init__(self,data_list):
        self.DataList=data_list
    # Need a Function to create a simple moving average of the data
    def get_simple_moving_average(self,average_number):
        sma=[]
        for i in range(len(self.DataList)-(average_number-1)):
            sum_data=0
            for j in range(average_number):
                sum_data=sum_data+self.DataList[i+j]
            sma.append(sum_data/average_number)
        return(sma)
    def get_exponential_moving_average(self,average_number):
        ema=[]
        k=2/(average_number+1)
        for i in range(len(self.DataList)-(average_number-1)):
            if i==0:
                sum=0
                for j in range(average_number):
                    sum=sum+self.DataList[j]
                first_entry=sum/average_number
                ema.append(first_entry)
            else:
                next_entry=k*self.DataList[i+(average_number-1)] + (1-k)*ema[i-1]
                ema.append(next_entry)
        return(ema)




# Function that produces a list of Bars for a stock from a start date to an end date
def read_daily_bars(symbol_ticker,start_date,end_date):
    df=web.DataReader(symbol_ticker,'yahoo',start_date,end_date)
    print(df.index[0])
    list_daily_bars=[]
    for i in range(len(df)):
        list_daily_bars.append(Daily_Bar(df['Open'][i],df['High'][i],df['Low'][i],df['Close'][i],df.index[i],df['Volume'][i]))
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
    return((Bar(year_open,year_high,year_low,year_close,year_volume),Bar(average_open,average_high,average_low,average_close,average_volume),symbol))

# Want to plot close values of a stock for a period of time
def plot_closes(symbol,start_date,end_date):
    # Create a list of daily bars for the stock
    list_daily_bars=read_daily_bars(symbol,start_date,end_date)

    # Create the x data of datetime objects for my line chart
    list_timestamp_dates=get_list('Date',list_daily_bars)
    x=timestamp_to_datetime(list_timestamp_dates)

    # Create the y data as a list of closes
    y=get_list('Close',list_daily_bars)

    # Create the line for our plot and make it an appropriate data frame
    trace1=go.Scatter(x=x,y=y)
    data=go.Data([trace1])

    # Giving appropriate title to the plot and axis
    layout=go.Layout(title=symbol + ' closes from ' + make_string_date(start_date) + ' to '+make_string_date(end_date),
                     xaxis=dict(title='Date'),
                     yaxis=dict(title='Price'))

    fig=go.Figure(data=data,layout=layout)
    # Create plot with appropriate name in plotly
    py.plot(fig,filename=symbol + ' closes from ' + make_string_date(start_date) + ' to '+make_string_date(end_date))

# Creates a candlestick figure and returns it
def construct_candlestick_plot(symbol,start_date,end_date):
    # Fetch the data from yahoo
    df=web.DataReader(symbol,'yahoo',start_date,end_date)

    # Create initial candlestick figure
    fig=FF.create_candlestick(df.Open,df.High,df.Low,df.Close,dates=df.index)

    # Add graph and axis titles
    fig['layout'].update({'title':'Candlestick Plot',
                          'yaxis':{'title':'Stock Price'},
                          'xaxis':{'title':'Date'}})
    return(fig)

# Add a sma line to a plot
def add_sma_line(fig,data_list,x_values,average_length):
    # Create values for the sma line
    data_series=DataSeries(data_list)
    sma_list=data_series.get_simple_moving_average(average_length)

    # Select appropriate x values to pair with the sma values
    x=[]
    for i in range(average_length-1,len(x_values)):
        x.append(x_values[i])

    # Create points to plot
    add_line= go.Scatter(x=x,y=sma_list,name='sma('+str(average_length)+')')

    # Add the line to the Figure
    fig['data'].extend([add_line])
    return(fig)

# Add an ema line to a plot
def add_ema_line(fig,data_list,x_values,average_length):
    #Create values for the ema line
    data_series=DataSeries(data_list)
    ema_list=data_series.get_exponential_moving_average(average_length)

    # Select appropriate x values to pair with the ema values
    x=[]
    for i in range(average_length-1,len(x_values)):
        x.append(x_values[i])

    # Create points to plot
    add_line=go.Scatter(x=x,y=ema_list,name='ema('+str(average_length)+')')

    # Add line to figure
    fig['data'].extend([add_line])
    return(fig)



# Plot the candlestick plot for given symbol between given dates
def plot_candlestick_plot(symbol,start_date,end_date):
    # Create appropriate candlestick figure
    fig=construct_candlestick_plot(symbol,start_date,end_date)

    # Plot the figure
    py.plot(fig,filename=symbol + ' Candlestick Plot')

def plot_candlestick_with_sma(symbol,start_date,end_date,average_length):
    # Create the candlestick plot without the moving average
    fig=construct_candlestick_plot(symbol,start_date,end_date)

    # Fetch appropriate data from yahoo
    df=web.DataReader(symbol,'yahoo',start_date,end_date)

    # Add the sma line to the figure
    add_sma_line(fig,df.Close,df.index,average_length)
    py.plot(fig,filename='Candlestick with sma plot for '+symbol)


def plot_candlestick_with_sma_ema(symbol,start_date,end_date,average_length):
    # Create the candlestick plot without the moving average
    fig=construct_candlestick_plot(symbol,start_date,end_date)

    # Fetch appropriate data from yahoo
    df=web.DataReader(symbol,'yahoo',start_date,end_date)

    # Add the sma and ema lines to the figure
    add_ema_line(fig, df.Close, df.index, average_length)
    add_sma_line(fig,df.Close,df.index,average_length)

    py.plot(fig,filename='Candlestick with sma and ema plot for '+symbol)

today = datetime.date.today()
last_year = today - datetime.timedelta(days=365)

#print(analyse_recent_year('AAPL'))
#plot_closes('AAPL',last_year,today)
#plot_candlestick_plot('AAPL',last_year,today)
#plot_candlestick_with_sma('AAPL',last_year,today,30)
#plot_candlestick_with_sma_ema('AAPL',last_year,today,30)

data=[22.27,22.19,22.08,22.17,22.18,22.13,22.23,22.43,22.24,22.29,22.15,22.39,22.38,22.61,23.36,24.05,23.75,23.83,23.95,23.63,23.82,23.87,23.65,23.19,23.1,23.33,22.68,23.1,22.4,22.17]
data_series=DataSeries(data)
#print(data_series.get_exponential_moving_average(10))