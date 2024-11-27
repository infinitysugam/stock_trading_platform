from django.shortcuts import render

import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import requests

def home(request):
        return render(request,'order_home.html')


def order_book_view(request):
        accountID = "101-001-29894202-001"
        token="d6214def02031bec4369cb5ed02b8d8f-811f3087858ea0d03027ba6d5f34a968"
        api = API(access_token=token)
        instrument  = request.GET.get("instrument","EUR_USD")
        params ={
                "instruments": instrument
                }
        r = pricing.PricingInfo( accountID=accountID,params=params)
        rv = api.request(r)
        data= r.response
        #print(r.response)
            # Extract bids and asks
        bids = data['prices'][0]['bids']
        asks = data['prices'][0]['asks']


        asks = sorted(asks, key=lambda x: float(x['price']), reverse=True)

    # Sort bids by lowest to highest
        bids = sorted(bids, key=lambda x: float(x['price']),reverse=True)

    # Calculate spread (lowest ask - highest bid) without rounding
        lowest_ask = float(asks[-1]['price'])  # Last item in asks (lowest price)
        highest_bid = float(bids[-1]['price'])  # Last item in bids (highest price)
        spread = f"{lowest_ask - highest_bid:.6f}"


        # Pass data to template
        context = {
                'bids': bids,
                'asks': asks,
                'spread':spread,
        }
        return render(request, 'order_book.html', context)

