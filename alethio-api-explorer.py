from ens import ENS
from web3 import Web3
import requests
import argparse

class alethioAPI:
    """Alethio API wrapper."""

    def __init__(self, provider):
        """ Initialize instance of alethioAPI. """
        self.w3 = Web3(Web3.HTTPProvider(provider))
    
    def getEthBalance(self, ethAddress):
        """ Get Ether Balance for current address."""
        response = requests.get(f'https://api.aleth.io/v1/accounts/{ethAddress}')
        return self.w3.fromWei(int(response.json()['data']['attributes']['balance']),'ether')

    def getERC20Balances(self, ethAddress):
        """ Get ERC-20 token balances for current address. """
        response = requests.get('https://blockscout.com/eth/mainnet/api?module=account&action=tokenlist&address='+ethAddress)
        return response.json()['result']
    

parser = argparse.ArgumentParser(description="Learn about an ETH address")
parser.add_argument('--address', '-a', help='An Ethereum address of the form 0x1a2b3c...')
parser.add_argument('--provider', help='A preferred web3 HTTP provider for interacting with the blockchain; defaults to infura mainnet', default='https://mainnet.infura.io')
parser.add_argument('--ens', help='A human readable Ethereum address based on the ENS')
args = parser.parse_args()

api = alethioAPI(args.provider)
if args.ens:
    ns = ENS.fromWeb3(api.w3)
    ethAddress = ns.address(args.ens)
elif args.address:
    ethAddress = args.address
    
print('Ether balance: '+ str(api.getEthBalance(ethAddress)))
for token in api.getERC20Balances(ethAddress):
    print('Symbol: ' + token['symbol'] + ', Token: ' + token['name'] + ', Amount: ' + str(api.w3.fromWei(int(token['balance']),'ether')))
