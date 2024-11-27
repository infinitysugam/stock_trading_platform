from django.shortcuts import render,redirect
from django.core.paginator import Paginator


import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import requests

from .models import Order

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
        # r = pricing.PricingInfo( accountID=accountID,params=params)
        # rv = api.request(r)
        # data= r.response

        data = {'time': '2024-11-27T03:39:05.484480122Z', 'prices': [{'type': 'PRICE', 'time': '2024-11-27T03:38:53.879293682Z', 'bids': [{'price': '1.04818', 'liquidity': 500000}, {'price': '1.04817', 'liquidity': 2500000}, {'price': '1.04816', 'liquidity': 2000000}, {'price': '1.04815', 'liquidity': 5000000}, {'price': '1.04812', 'liquidity': 10000000}, {'price': '1.04809', 'liquidity': 10000000}], 'asks': [{'price': '1.04833', 'liquidity': 500000}, {'price': '1.04834', 'liquidity': 500000}, {'price': '1.04835', 'liquidity': 2000000}, {'price': '1.04836', 'liquidity': 2000000}, {'price': '1.04837', 'liquidity': 5000000}, {'price': '1.04839', 'liquidity': 10000000}, {'price': '1.04842', 'liquidity': 10000000}], 'closeoutBid': '1.04809', 'closeoutAsk': '1.04842', 'status': 'tradeable', 'tradeable': True, 'quoteHomeConversionFactors': {'positiveUnits': '1.00000000', 'negativeUnits': '1.00000000'}, 'instrument': 'EUR_USD'}]}
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

        if request.method == "POST":
                order_type = request.POST.get("order_type")
                order_instrument = request.POST.get("instrument")
                order_price = float(request.POST.get("price"))
                order_quantity = float(request.POST.get("quantity"))

                #print(order_price,order_quantity)


                status = "pending"
                filled_quantity = 0

                # Buy Order Logic
                if order_type == "buy":
                        for ask in asks:
                                ask_price = float(ask["price"])
                                ask_liquidity = int(ask["liquidity"])

                                if ask_price == order_price:  # Check for matching sellers
                                        if ask_liquidity >= order_quantity:  # Fully filled
                                                status = "filled"
                                                filled_quantity = order_quantity
                                                break
                                        else:
                                                status="partially_filled"
                                                filled_quantity = ask_liquidity
                                                break
                                else:  # Partially filled
                                        status = "pending"
                                        filled_quantity = 0 


        # Sell Order Logic
                elif order_type == "sell":
                        for bid in bids:
                                bid_price = float(bid["price"])
                                bid_liquidity = int(bid["liquidity"])

                                if bid_price == order_price: 
                                         # Check for matching buyers
                                        if bid_liquidity >= order_quantity:  # Fully filled
                                                status = "filled"
                                                filled_quantity = order_quantity
                                                break
                                        else:
                                                status="partially_filled"
                                                filled_quantity = bid_liquidity
                                                break
                                else:  # Partially filled               
                                        status = "pending"
                                        filled_quantity = 0


                Order.objects.create(
                order_type=order_type,
                instrument=order_instrument,
                price=order_price,
                quantity=order_quantity,  # Original quantity
                filled_quantity=filled_quantity,
                status=status,
        )

                # Redirect back to the order book view after placing the order
                return redirect('order_management')
        
        orders = Order.objects.all().order_by('-timestamp')
        paginator = Paginator(orders, 10) 
        page_number = request.GET.get('page')  
        page_obj = paginator.get_page(page_number) 
        # Pass data to template
        context = {
                'bids': bids,
                'asks': asks,   
                'spread':spread,
                'instrument':instrument,
                'page_obj':page_obj,
        }
        return render(request, 'order_book.html', context)

