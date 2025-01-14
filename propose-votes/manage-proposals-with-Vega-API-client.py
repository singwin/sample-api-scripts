#!/usr/bin/python3

"""
Script language: Python3

Talks to:
- Vega node (gRPC)

Apps/Libraries:
- Vega-API-client (https://pypi.org/project/Vega-API-client/)

Responses:
- response-examples.txt
"""

# Note: this file uses smart-tags in comments to section parts of the code to
# show them as snippets in our documentation. They are not necessary to be
# included when creating your own custom code.
#
# Example of smart-tags:
#  __something:
# some code here
# :something__

import requests
import helpers
import os

node_url_grpc = os.getenv("NODE_URL_GRPC")
if not helpers.check_var(node_url_grpc):
    print("Error: Invalid or missing NODE_URL_GRPC environment variable.")
    exit(1)

wallet_server_url = os.getenv("WALLETSERVER_URL")
if not helpers.check_url(wallet_server_url):
    print("Error: Invalid or missing WALLETSERVER_URL environment variable.")
    exit(1)

wallet_name = os.getenv("WALLET_NAME")
if not helpers.check_var(wallet_name):
    print("Error: Invalid or missing WALLET_NAME environment variable.")
    exit(1)

wallet_passphrase = os.getenv("WALLET_PASSPHRASE")
if not helpers.check_var(wallet_passphrase):
    print("Error: Invalid or missing WALLET_PASSPHRASE environment variable.")
    exit(1)

# Help guide users against including api version suffix on url
wallet_server_url = helpers.check_wallet_url(wallet_server_url)

# __import_client:
import vegaapiclient as vac

# Vega gRPC clients for reading/writing data
data_client = vac.VegaTradingDataClient(node_url_grpc)
# :import_client__

#####################################################################################
#                           W A L L E T   S E R V I C E                             #
#####################################################################################

print(f"Logging into wallet: {wallet_name}")

# Log in to an existing wallet
req = {"wallet": wallet_name, "passphrase": wallet_passphrase}
response = requests.post(f"{wallet_server_url}/api/v1/auth/token", json=req)
helpers.check_response(response)
token = response.json()["token"]

assert token != ""
print("Logged in to wallet successfully")

# List key pairs and select public key to use
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{wallet_server_url}/api/v1/keys", headers=headers)
helpers.check_response(response)
keys = response.json()["keys"]
pubkey = keys[0]["pub"]

assert pubkey != ""
print("Selected pubkey for signing")

#####################################################################################
#                            L I S T   P R O P O S A L S                            #
#####################################################################################

# __get_proposals:
# Request a list of proposals on a Vega network
request = vac.data_node.api.v1.trading_data.GetProposalsRequest()
proposals = data_client.GetProposals(request)
print("Proposals:\n{}".format(proposals))
# :get_proposals__

proposalID = proposals.data[0].proposal.id
assert proposalID != ""
print(f"Proposal found: {proposalID}")

#####################################################################################
#                         P R O P O S A L   D E T A I L S                           #
#####################################################################################

# __get_proposal_detail:
# Request results of a specific proposal on a Vega network
request = vac.data_node.api.v1.trading_data.GetProposalByIDRequest(proposal_id=proposalID)
proposal = data_client.GetProposalByID(request)
print("Proposal:\n{}".format(proposal))
# :get_proposal_detail__

#####################################################################################
#                          P A R T Y   P R O P O S A L S                            #
#####################################################################################

# __get_proposals_by_party:
# Request a list of proposals for a party (pubkey) on a Vega network
request = vac.data_node.api.v1.trading_data.GetProposalsByPartyRequest(party_id=pubkey)
party_proposals = data_client.GetProposalsByParty(request)
print("Party proposals:\n{}".format(party_proposals))
# :get_proposals_by_party__
