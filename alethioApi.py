from ens import ENS
from web3 import Web3
import requests
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class alethioAPI:
    """Alethio API wrapper."""

    def __init__(self, provider="https://mainnet.infura.io"):
        """ Initialize instance of alethioAPI. """
        self.w3 = Web3(Web3.HTTPProvider(provider))
    
    def getEthBalance(self, ethAddress):
        """ Get Ether Balance for current address."""
        response = requests.get(f'https://api.aleth.io/v1/accounts/{ethAddress}')
        logging.info(response.json())
        return self.w3.fromWei(int(response.json()['data']['attributes']['balance']),'ether')

    def getERC20Balances(self, ethAddress):
        """ Get ERC-20 token balances for current address. """
        response = requests.get('https://blockscout.com/eth/mainnet/api?module=account&action=tokenlist&address='+ethAddress)
        logging.info(response.json())
        return response.json()['result']
    
