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
    def __init__(self,data_list,date_list):
        self.Data=data_list
        self.Dates=date_list

    # Need a Function to create a simple moving average of the data
    def sma(self, average_number):
        # Calculating the sma list
        # Also want to calculate the respective dates for the sma
        new_dates=[]
        sma=[]
        # For clause for each entry in lists for new data
        for i in range(len(self.Data)-(average_number-1)):
            # Set and reset the variable sum data for each calculation
            sum_data=0
            # Another for clause to calculate the relevant sum for each entry
            for j in range(average_number):
                sum_data=sum_data+self.Data[i+j]
            # Add relevant date to the list
            new_dates.append(self.Dates[i+average_number-1])
            # Add the sma value to our list
            sma.append(sum_data/average_number)
        # Return another data series with dat as the sma values and corresponding dates
        return(DataSeries(sma,new_dates))

    # Need a function to create exponential moving average dataseries of the dataseries we have
    #Follows similar to sma but with relevant ema calculations
    def ema(self, average_number):
        ema=[]
        new_dates=[]
        k=2/(average_number+1)
        for i in range(len(self.Data)-(average_number-1)):
            new_dates.append(self.Dates[i+average_number-1])
            if i==0:
                sum=0
                for j in range(average_number):
                    sum=sum+self.Data[j]
                first_entry=sum/average_number
                ema.append(first_entry)
            else:
                next_entry=k*self.Data[i+(average_number-1)] + (1-k)*ema[i-1]
                ema.append(next_entry)
        return(DataSeries(ema,new_dates))

