import stock_mini_functions as smf
import plotly.graph_objs as go
import pandas_datareader.data as web
from plotly.tools import FigureFactory as FF
import stock_classes as sc
import plotly.plotly as py
import datetime

# Want to plot close values of a stock for a period of time
def plot_closes(symbol,start_date,end_date):
    # Create a list of daily bars for the stock
    list_daily_bars=smf.read_daily_bars(symbol,start_date,end_date)

    # Create the x data of datetime objects for my line chart
    list_timestamp_dates=smf.get_list('Date',list_daily_bars)
    x=smf.timestamp_to_datetime(list_timestamp_dates)

    # Create the y data as a list of closes
    y=smf.get_list('Close',list_daily_bars)

    # Create the line for our plot and make it an appropriate data frame
    trace1=go.Scatter(x=x,y=y)
    data=go.Data([trace1])

    # Giving appropriate title to the plot and axis
    layout=go.Layout(title=symbol + ' closes from ' + smf.make_string_date(start_date) + ' to '+smf.make_string_date(end_date),
                     xaxis=dict(title='Date'),
                     yaxis=dict(title='Price'))

    fig=go.Figure(data=data,layout=layout)
    # Create plot with appropriate name in plotly
    py.plot(fig,filename=symbol + ' closes from ' + smf.make_string_date(start_date) + ' to '+smf.make_string_date(end_date))

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
    data_series=sc.DataSeries(data_list,x_values)
    sma_data=data_series.sma(average_length)
    sma_list=sma_data.Data

    # Select appropriate x values to pair with the sma values
    x=[]
    for i in range(average_length-1,len(data_series.Dates)):
        x.append(data_series.Dates[i])

    # Create points to plot
    add_line= go.Scatter(x=x,y=sma_list,name='sma('+str(average_length)+')')

    # Add the line to the Figure
    fig['data'].extend([add_line])
    return(fig)

# Add an ema line to a plot
def add_ema_line(fig,data_list,x_values,average_length):
    #Create values for the ema line
    data_series=sc.DataSeries(data_list,x_values)
    ema_data=data_series.ema(average_length)
    ema_list=ema_data.Data

    # Select appropriate x values to pair with the ema values
    x=[]
    for i in range(average_length-1,len(data_series.Dates)):
        x.append(data_series.Dates[i])

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

