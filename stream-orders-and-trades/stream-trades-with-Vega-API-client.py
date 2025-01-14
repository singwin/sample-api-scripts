#!/usr/bin/python3

"""
Script language: Python3

Talks to:
- Vega node (gRPC)

Apps/Libraries:
- gRPC (node): Vega-API-client (https://pypi.org/project/Vega-API-client/)
"""

# Note: this file uses smart-tags in comments to section parts of the code to
# show them as snippets in our documentation. They are not necessary to be
# included when creating your own custom code.
#
# Example of smart-tags:
#  __something:
# some code here
# :something__

import os
import signal
import sys

# __import_client:
import vegaapiclient as vac
# :import_client__

node_url_grpc = os.getenv("NODE_URL_GRPC")

def signal_handler(sig, frame):
    print('Exit requested.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# __create_client:
# Create a Vega gRPC data client
data_client = vac.VegaTradingDataClient(node_url_grpc)
# :create_client__

# __find_market:
# Get a list of markets, and select the first market returned
markets = data_client.Markets(vac.data_node.api.v1.trading_data.MarketsRequest()).markets
market_id = markets[0].id
# :find_market__

# __stream_trades:
# Subscribe to the Trades stream for the marketID specified
# Optional: Market identifier - filter by market
#            Party identifier - filter by party
# By default, all trades on all markets for all parties will be returned on the stream.
subscribe_request = vac.data_node.api.v1.trading_data.TradesSubscribeRequest(market_id=market_id)
for stream_resp in data_client.TradesSubscribe(subscribe_request):
    for trade in stream_resp.trades:
        # All trades arriving over the channel/stream will be printed
        print(trade)
# :stream_trades__


