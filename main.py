from ens import ENS
import argparse
import alethioApi

parser = argparse.ArgumentParser(description="Learn about an ETH address")
parser.add_argument('--address', '-a', help='An Ethereum address of the form 0x1a2b3c...')
parser.add_argument('--provider', help='A preferred web3 HTTP provider for interacting with the blockchain; defaults to infura mainnet', default='https://mainnet.infura.io')
parser.add_argument('--ens', help='A human readable Ethereum address based on the ENS')
parser.add_argument('--logLevel', '-ll', help='Set logging level (i.e. DEBUG, INFO, WARNING, etc.)', default='WARNING')
args = parser.parse_args()

api = alethioApi.alethioAPI(args.provider, args.logLevel)
if args.ens:
    ns = ENS.fromWeb3(api.w3)
    ethAddress = ns.address(args.ens)
elif args.address:
    ethAddress = args.address
    
print('Ether balance: '+ str(api.getEthBalance(ethAddress)))
for token in api.getERC20Balances(ethAddress):
    print('Symbol: ' + token['symbol'] + ', Token: ' + token['name'] + ', Amount: ' + str(api.w3.fromWei(int(token['balance']),'ether')))
for trxn in api.getEthTransfers(ethAddress):
    print('Amount: ' + str(api.w3.fromWei(int(trxn['attributes']['total']),'ether')))
for trxn in api.getTokenTransfers(ethAddress):
    print('Amount: ' + str(api.w3.fromWei(int(trxn['attributes']['value']),'ether')) + ' Token: ' + trxn['attributes']['symbol'])

