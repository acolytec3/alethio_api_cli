import argparse
import alethioApi

parser = argparse.ArgumentParser(description="Learn about an ETH address")
parser.add_argument('--address', '-a', help='An ENS address or Ethereum address')
parser.add_argument('--provider', help='A preferred web3 HTTP provider for interacting with the blockchain; defaults to infura mainnet', default='https://mainnet.infura.io')
parser.add_argument('--logLevel', '-ll', help='Set logging level (i.e. DEBUG, INFO, WARNING, etc.)', default='WARNING')
parser.add_argument('--tokens', '-t', help="Flag to show tokens and values associated with provided address", action='store_true')
parser.add_argument('--ethTransfers', '-et', help='Flag to show Ether transfers associated with provided address', action='store_true')
parser.add_argument('--tokenTransfers','-tt', help='Flag to show token transfers associated with provided address', action='store_true')
parser.add_argument('--balance', '-b', help='Flag to show current Ether balance of address', action='store_true')
parser.add_argument('--contractMessages', '-cm', help='Flag to show Smart Contract interactions associated with provided address', action='store_true')

args = parser.parse_args()

api = alethioApi.alethioAPI(args.provider, args.logLevel)

if args.balance:
    print('Ether balance: '+ str(api.getEthBalance(args.address)))
if args.tokens:
    for token in api.getTokenBalances(args.address):
        if token['symbol']:
            print('Symbol: ' + token['symbol'] + ', Token: ' + token['name'] + ', Amount: ' + token['balance'])
        else:
            print('Contract: ' + token['contractAddress'] + ', Amount: ' + token['balance'])
if args.ethTransfers:
    for trxn in api.getEthTransfers(args.address):
        print('Amount: ' + trxn['attributes']['total'])
if args.tokenTransfers:
    for trxn in api.getTokenTransfers(args.address):
        print('Amount: ' + str(api.w3.fromWei(int(trxn['attributes']['value']),'ether')) + ' Token: ' + trxn['attributes']['symbol'])
if args.contractMessages:
    for trxn in api.getContractMessages(args.address):
        print('Message Type: ' + trxn['attributes']['msgType'] + ' Message to: ' + trxn['relationships']['to']['data']['id'])
