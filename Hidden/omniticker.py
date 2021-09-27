import requests
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import time
from datetime import date, datetime
import numpy as np
import math


response1 = None
json_data1 = None
payload, headers = {},{}

class omnitick():
    failures = 0
    attempts = 0
    startTime= datetime.now()
    bitcoin_org = None
##MISC FUNCTIONS
    def milbil(self,bignumber):
        if bignumber > 1000000000000:
            return '$'+ str(round(round(bignumber,-9)/1000000000000,2))+'T'
        elif bignumber > 1000000000:
            return '$'+ str(round(round(bignumber,-6)/1000000000,2))+'B'
        elif bignumber > 1000000:
            return '$'+ str(round(round(bignumber,-3)/1000000,2))+'M'
        return bignumber

        

    def __init__(self,window=None):
        url = "http://api.coincap.io/v2/assets"
    ##********FETCH DATA********##
        response = None
        json_data = None

        while json_data == None:
            self.attempts+=1
            try:
                response = requests.request("GET", url, headers=headers, data = payload)
                json_data = json.loads(response.text.encode('utf8')) 
            except Exception:
                self.failures+=1
                print('Query failure: '+str(self.failures)+'/'+str(self.attempts)+'. Attempting again in 10 seconds.')
                time.sleep(10)

        
        self.bitcoin_org = pd.DataFrame(json_data["data"])
        bitcoin_data = pd.DataFrame(json_data["data"])[['rank','name','symbol','priceUsd','changePercent24Hr','vwap24Hr','marketCapUsd']]


    ##***********FORMATTING******************##
        bitcoin_data['priceUsd'] = pd.to_numeric(bitcoin_data['priceUsd']).round(7)
        bitcoin_data['priceUsd'] = bitcoin_data['priceUsd'].apply(lambda x:'$' + str('{:,}'.format(x)))
        bitcoin_data['changePercent24Hr'] = pd.to_numeric(bitcoin_data['changePercent24Hr']).round(3)
        bitcoin_data['changePercent24Hr'] = bitcoin_data['changePercent24Hr'].apply(lambda x: str(x)+'%')
        bitcoin_data['vwap24Hr'] = pd.to_numeric(bitcoin_data['vwap24Hr']).round(4).apply(lambda x:'     $' + str('{:,}'.format(x)))
        bitcoin_data['marketCapUsd'] = bitcoin_data['marketCapUsd'].apply(lambda x:math.floor(float(x))).apply(lambda x: self.milbil(x))

        #!!!!!!!!!!!!!!!#format name column and drop others
        #bitcoin_data['name']= x for x inbitcoin_data[['rank','name','symbol']].apply(lambda x: str(x[0])+'. '+x[1]+'('+x[2]+')')
        
        gcmc = '${:,}'.format(math.floor(pd.DataFrame(json_data['data'])['marketCapUsd'].agg(lambda x:float(x)).sum()))

        '''
        print(pd.DataFrame(json_data['data']).info())
        
        #df = pd.DataFrame(bitcoin_data, columns=['time', 'priceUsd'])
        #df.to_csv('bitcoin-usd.csv', index=False)
        #df['priceUsd'] = pd.to_numeric(df['priceUsd'], errors='coerce').fillna(0, downcast='infer')

        #print(df.sample)
        #df.plot(x ='time', y='priceUsd', kind = 'line')
        #plt.show()
        '''


    ##***********UI******************##
        if window == None:
            window = tk.Tk()
            window.title('OmniTicker')

        window.minsize(1000,800)

        ##########!!!!!!!!##############fix leading zeroes
        shortDate= datetime.now()
        shortDate = str(shortDate.month)+'/'+str(shortDate.day)+'/'+str(shortDate.year)+' '+str(shortDate.hour)+':'+str(shortDate.minute)

        window.configure(bg='black')
        dLab= tk.Label(window, text=shortDate,font=("arial", 12),wraplength=100, bg='black', fg='#90EE90').grid(column=2, row=0)
        
        lbl = tk.Label(window, text=bitcoin_data.head(50).to_string(index=False,header=False),font=('verdana',9),wraplength=760, bg='black', fg='#90EE90').grid(column=0, row=1)
        
        lb3 = tk.Label(window, text='Crypto Market Cap:\n'+ gcmc,justify="left",font=("courier", 12), bg='black', fg='gold').grid(column=0, row=0)
        
        lbl2 = tk.Label(window, text=bitcoin_data.iloc[50:101].to_string(index=False,header=False),font=('verdana',9),wraplength=760,
                     bg='black', fg='#90EE90')
        lbl2.grid(column=2, row=1)

        window.after(18000,lambda: omnitick(window))
        window.mainloop()


omnitick()


###HISTORICAL DATA TEMPLATE API
'''
url1 = 'http://api.coincap.io/v2/assets/bitcoin/history?interval=1y'
try:
    response1 = requests.request("GET", url1, headers=headers, data = payload)
    json_data1 = json.loads(response1.text.encode('utf8'))
except Exception:
    print('fetch failed')
    

print(pd.DataFrame(json_data1['data']).head(40))
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 100 entries, 0 to 99
Data columns (total 12 columns):
 #   Column             Non-Null Count  Dtype 
---  ------             --------------  ----- 
 0   id                 100 non-null    object
 1   rank               100 non-null    object
 2   symbol             100 non-null    object
 3   name               100 non-null    object
 4   supply             100 non-null    object
 5   maxSupply          62 non-null     object
 6   marketCapUsd       100 non-null    object
 7   volumeUsd24Hr      100 non-null    object
 8   priceUsd           100 non-null    object
 9   changePercent24Hr  100 non-null    object
 10  vwap24Hr           100 non-null    object
 11  explorer           99 non-null     object
dtypes: object(12)
memory usage: 9.5+ KB
None              id  ...                                           explorer
0       bitcoin  ...                           https://blockchain.info/
1      ethereum  ...                              https://etherscan.io/
2       cardano  ...                       https://cardanoexplorer.com/
3        tether  ...             https://www.omniexplorer.info/asset/31
4  binance-coin  ...  https://etherscan.io/token/0xB8c77482e45F1F44d...
5           xrp  ...              https://xrpcharts.ripple.com/#/graph/
6        solana  ...                       https://explorer.solana.com/
7      usd-coin  ...  https://etherscan.io/token/0xa0b86991c6218b36c...
8      polkadot  ...                      https://polkascan.io/polkadot
9      dogecoin  ...               http://dogechain.info/chain/Dogecoin

[10 rows x 12 columns]
'''
