import urllib.request
#import sslimport
import json
import time
import tweepy
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
api_key = "3vzyzm2kncdvzirrvhxm4"




# Allows adding as many coins as desired
coin_list =[    "LTC",    "ETH",    "BTC"]
coins = ','.join(coin_list)

map = [{"name":""},{"symbol": ""},    {"price": " Price: "},    {"percent_change_24h": " - 24 Hour Percent Change: "},
{"market_cap": " Market Cap: "},    {"volume_24h": " 24 Hour Volume: "},    {"url_shares": " URL Shares: "},
{"reddit_posts": " Reddit Posts: "},    {"tweets": " Tweets: "},    {"galaxy_score": " Galaxy Score: "},    {"volatility": " Volatility: "},
{"social_volume": " Social Volume: "},    {"news": " News: "},    {"close": " Close: "},]

def final_render(asset_coin, value, key, asset):
    if key == 'symbol':
        asset_coin += " (" + asset[key] + ")"
    elif key == 'percent_change_24h':
        asset_coin += value + str(asset[key]) + "%"
    else:
        asset_coin += value + str(asset[key])
    return asset_coin

def main():
    url = "https://api.lunarcrush.com/v2?data=assets&key=" + api_key + "&symbol=" + coins
    assets = json.loads(urllib.request.urlopen(url).read())
    for asset in assets['data']:
        asset_coin = ""
        for field in map:
            key = list(field.keys())[0]
            value = list(field.values())[0]
            asset_coin = final_render(asset_coin, value, key, asset)
            print(asset_coin)
            print(len(asset_coin))
# Runs main() every 30 minutes
while True:
    main()
    time.sleep(1800)
