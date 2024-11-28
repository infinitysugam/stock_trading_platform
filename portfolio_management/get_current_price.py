import requests
import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import requests


def price(instrument_list):
        
        accountID = "101-001-29894202-001"
        token="d6214def02031bec4369cb5ed02b8d8f-811f3087858ea0d03027ba6d5f34a968"
        api = API(access_token=token)
        params ={
                "instruments": "EUR_USD,EUR_JPY,GBP_USD,USD_JPY,AUD_USD"
                }
        r = pricing.PricingInfo( accountID=accountID,params=params)
        rv = api.request(r)
        data= r.response


        current_prices = {}

        for price_data in data['prices']:
            instrument = price_data['instrument']
            highest_bid = float(price_data['bids'][0]['price'])
            lowest_ask = float(price_data['asks'][0]['price'])

            # Calculate the mid-price
            mid_price = (highest_bid + lowest_ask) / 2

            # Store the mid-price in the dictionary
            current_prices[instrument] = mid_price
        
        return current_prices
        
