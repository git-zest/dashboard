import pandas as pd 
import numpy as np
import random


class SimData:
    '''
    This is an example of how my data is going to look like from my scripts that automatically fetch data
    '''
    def __init__(self,path):
        #reading csv
        self.df = pd.read_csv(path)
        #we dont need adjusted close or volume
        self.df = self.df.drop(self.df.columns[-2:], axis=1)
        #keeping track of the current position
        self.pos =0
    
    def get_next_row(self): # This simulates the data being fetched from the internet
        #if position not greater than length of dataframe
        if self.pos < len(self.df):
            self.pos += 1

            #returning the next row and the decision to buy or sell
            return np.array(self.df.iloc[self.pos-1]) , self.decide_buy_sell()
        else:

            return None

    def decide_buy_sell(self):
        return random.randint(0,2)
    
    # this method is used in the Callback to fetch next row
    def get_next_pandas_row(self):
        open_high_low_close, purchase_decision = self.get_next_row() #get new row
        new_row = [{"Date": str(open_high_low_close[0]), "Open": open_high_low_close[1], "High": open_high_low_close[2], 
                "Low": open_high_low_close[3], "Close" : open_high_low_close[4], "Purchase_Decision" : purchase_decision}]
        pd_row = pd.DataFrame(new_row) # convert the data into pandas row
        return pd_row # return row