import requests
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import time
from datetime import date, datetime
import numpy as np


window = None


url = "http://api.coincap.io/v2/assets"

payload, headers = {},{}

buttbool = False



def omnitick(window):

    try:
        window.destroy()
    except Exception:
        print('no window')

    
    response = None
    json_data = None

    while json_data == None:
        try:
            response = requests.request("GET", url, headers=headers, data = payload)
            json_data = json.loads(response.text.encode('utf8'))
        except Exception:
            print('fetch failed')
            time.sleep(6)

    bitcoin_data = pd.DataFrame(json_data["data"]).set_index('name')
    bitcoin_data = bitcoin_data[['symbol','rank','priceUsd']]
    bitcoin_data['priceUsd'] = pd.to_numeric(bitcoin_data['priceUsd']).round(8)


    #df = pd.DataFrame(bitcoin_data, columns=['time', 'priceUsd'])
    #df.to_csv('bitcoin-usd.csv', index=False)
    #df['priceUsd'] = pd.to_numeric(df['priceUsd'], errors='coerce').fillna(0, downcast='infer')

    #print(df.sample)
    #df.plot(x ='time', y='priceUsd', kind = 'line')
    #plt.show()
    window = tk.Tk()

    window.title('OmniTicker')

    dLab= tk.Label(window, text=str(datetime.now())).grid(column=0, row=0)
    lbl = tk.Label(window, text=bitcoin_data.head(50).to_string(index=False,header=None),justify="left",font="helvetica 11",wraplength=500)
    lbl.grid(column=0, row=1)
    lbl2 = tk.Label(window, text=bitcoin_data.iloc[50:101].to_string(index=False,header=None),justify="center",font="helvetica 11",wraplength=500)
    lbl2.grid(column=1, row=1)
    if buttbool == True:
        button = tk.Button(window, 
                           text="Refresh", 
                           fg="Green",
                           command=lambda:omnitick(window))
        button.grid(column=0, row=2)

    window.after(6000,lambda: omnitick(window))
    window.mainloop()




omnitick(window)
