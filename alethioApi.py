from ens import ENS
from web3 import Web3
import requests
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class alethioAPI:
    """Alethio API wrapper."""

    def __init__(self, provider="https://mainnet.infura.io", loggingLevel='WARNING'):
        """ Initialize instance of alethioAPI. """
        self.w3 = Web3(Web3.HTTPProvider(provider))
        logging.basicConfig(stream=sys.stdout, level=logging.getLevelName(loggingLevel))
    
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

    def getEthTransfers(self, ethAddress):
        """Get Ether transfers associated with current address. """
        response = requests.get(f'https://api.aleth.io/v1/accounts/{ethAddress}/etherTransfers')
        logging.info(response.json()['data'])
        return response.json()['data']

    def getTokenTransfers(self, ethAddress):
        """Get Ether transfers associated with current address. """
        response = requests.get(f'https://api.aleth.io/v1/accounts/{ethAddress}/tokenTransfers')
        logging.info(response.json()['data'])
        return response.json()['data']