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
import sys

#import lunarcrush




class omnitick():
    '''Omniticker is a lightweight desktop cryptocurrecy market tracker. This will become comphrensive tracker of all financial markets. I send my thanks to the CoinCapAPI developers.'''

###***CLASS ATTRIBUTES***###
    failures, attempts = 0,0
    startTime= datetime.now()
    payload, headers, BTC_HIS_payload, BTC_HIS_headers = {},{},{},{}
    capURL = 'http://api.coincap.io/v2/assets'
    capBTChisURL = 'api.coincap.io/v2/assets/bitcoin/history?interval=d1'
    response = None
    json_data = None
    window = None
    bitcoin_data = None
    gcmc=[]

###***METHODS***###

    def milbil(self,bignumber):
        if bignumber > 1000000000000: return '$'+ str(round(round(bignumber,-9)/1000000000000,2))+'T'
        elif bignumber > 1000000000:  return '$'+ str(round(round(bignumber,-6)/1000000000,2))+'B'
        elif bignumber > 1000000:     return '$'+ str(round(round(bignumber,-3)/1000000,2))+'M'
        return bignumber

    def fetchCoinCap(self):
        print('fCC')
###GET###
        while self.json_data == None:
            self.attempts+=1
            try:
                self.response = requests.request("GET", self.capURL, headers=self.headers, data = self.payload)
                self.json_data = json.loads(self.response.text.encode('utf8'))
            except Exception as ex:
                print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(ex).__name__, ex.args))
                self.failures+=1
                print('MARKET Query failure: '+str(self.failures)+'/'+str(self.attempts)+'. Attempting again in 9.001 seconds.')
                time.sleep(10)

##***********FORMATTING******************##
        self.gcmc.append('${:,}'.format(math.floor(pd.DataFrame(self.json_data['data'])['marketCapUsd'].agg(lambda x:float(x)).sum())))
        self.bitcoin_data = pd.DataFrame(self.json_data["data"])[['rank','name','symbol','priceUsd','changePercent24Hr','vwap24Hr','marketCapUsd']]

        sList=[]
        for x in self.bitcoin_data[['rank','name','symbol']].iterrows(): sList.append(x[1][0]+'. '+x[1][1]+' ('+x[1][2]+')')
        self.bitcoin_data['name']=pd.DataFrame(sList)
        self.bitcoin_data.drop(['rank','symbol'],axis=1,inplace=True)

        self.bitcoin_data['priceUsd'] = pd.to_numeric(self.bitcoin_data['priceUsd']).round(7)
        self.bitcoin_data['priceUsd'] = self.bitcoin_data['priceUsd'].apply(lambda x:'$' + str('{:,}'.format(x)))

        self.bitcoin_data['changePercent24Hr'] = pd.to_numeric(self.bitcoin_data['changePercent24Hr']).round(3)
        self.bitcoin_data['changePercent24Hr'] = self.bitcoin_data['changePercent24Hr'].apply(lambda x: str(x)+'%')

        self.bitcoin_data['vwap24Hr'] = pd.to_numeric(self.bitcoin_data['vwap24Hr']).round(4).apply(lambda x:'$' + str('{:,}'.format(x)))
        self.bitcoin_data['marketCapUsd'] = self.bitcoin_data['marketCapUsd'].apply(lambda x:math.floor(float(x))).apply(lambda x: self.milbil(x))

    def fetchLunarCrush(self):
        pass

    def btcHistoric(self):
            while self.json_data == None:
                self.attempts+=1
                try:
                    self.response = requests.request("GET", self.capBTChisURL, headers=self.BTC_HIS_headers, data = self.BTC_HIS_payload)
                    self.json_data = json.loads(self.response.text.encode('utf8'))
                except Exception:
                    self.failures+=1
                    print('HISTORIC Query failure: '+str(self.failures)+'/'+str(self.attempts)+'. Attempting again in 10 seconds.')
                    time.sleep(10)

    def displayWindow(self):

        shortDate= datetime.now()
        shortDate = shortDate.strftime("%B")+' '+str(shortDate.day)+' '+str(shortDate.year)+' '+str(shortDate.strftime("%I:%M:%S %p"))

        self.window.configure(bg='black')
        dtLab= tk.Label(self.window, text=shortDate,font=("arial", 12), bg='black', fg='#90EE90').grid(column=0, row=0)
        crypcaplab = tk.Label(self.window, text='Crypto Market Cap:\n'+ self.gcmc[-1],justify="left",font=("courier", 12), bg='black', fg='gold').grid(column=0, row=1)


        #!!!!!!!!!!!!!!!!!TKINTER LABELS FOR EACH ITEM
        cryptocol1=[]
        for x in self.bitcoin_data.iterrows():
            x=x[1]
            for z in range(len(x)):
                cryptocol1.append(tk.Label(self.window,text=x[z],font=('verdana',9), bg='black', fg='#90EE90'))

        #        for y in x:
        #            rng=range(0,len(x.columns))
        #            print(str(y[z]) for z in rng)
            #cryptocol1.append(tk.Label(,font=('verdana',9) bg='black', fg='#90EE90'))

        lbl = tk.Label(self.window, text=self.bitcoin_data.head(50).to_string(index=False,header=False),font=('verdana',9),wraplength=760, bg='black', fg='#90EE90').grid(column=0, row=2)

        lbl2 = tk.Label(self.window, text=self.bitcoin_data.iloc[50:101].to_string(index=False,header=False),font=('verdana',9),wraplength=760, bg='black', fg='#90EE90').grid(column=2, row=2)

        self.window.protocol("WM_DELETE_WINDOW", exec('sys.exit(0)'))
        self.window.mainloop()


    def __init__(self):

        self.window = tk.Tk()
        ###***FAKE MENUS***###
        '''
        menubar = tk.Menu(self.window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=None)
        filemenu.add_command(label="Open", command=None)
        filemenu.add_command(label="Save", command=None)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.window.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_command(label="New", command=None)
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Edit", command=None)
        menubar.add_cascade(label="Edit", menu=editmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=None)
        helpmenu.add_command(label="About...", command=None)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.window.config(menu=menubar)
'''
        self.window.minsize(1000,770)
        self.window.title('OmniTicker')
        self.window.iconphoto(True,tk.PhotoImage(file='btc2.bmp'))

        while True:
            self.fetchCoinCap()
            self.displayWindow()
            time.sleep(5)









##***********UI******************##






###HISTORICAL DATA TEMPLATE API AND coincap dataframe attributes
'''
url1 = 'http://api.coincap.io/v2/assets/bitcoin/history?interval=1y'

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
