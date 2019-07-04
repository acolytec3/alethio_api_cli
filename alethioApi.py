from ens import ENS
from web3 import Web3
import requests
import logging
import sys


class alethioAPI:
    """Alethio API wrapper."""

    def __init__(self, provider="https://mainnet.infura.io", loggingLevel='WARNING'):
        """ Initialize instance of alethioAPI. """
        self.w3 = Web3(Web3.HTTPProvider(provider))
        logging.basicConfig(stream=sys.stdout, level=logging.getLevelName(loggingLevel))
    
    def ENStoEthAddress(self, ens):
        """ Convert ENS address to standard Ethereum address. """
        if self.w3.isConnected():
            ns = ENS.fromWeb3(self.w3)
            return ns.address(ens)
        else:
            raise Exception('Web3 not connected.')

    def getEthBalance(self, ethAddress):
        """ Get Ether Balance for current address."""
        response = requests.get(f'https://api.aleth.io/v1/accounts/{ethAddress}')
        logging.info(response.json())
        return self.w3.fromWei(int(response.json()['data']['attributes']['balance']),'ether')

    def getTokenBalances(self, ethAddress):
        """ Get token balances for current address. Note: This function does not return tokens with a zero balance. """
        response = requests.get('https://blockscout.com/eth/mainnet/api?module=account&action=tokenlist&address='+ethAddress)
        logging.info(response.json())
        tokens = response.json()['result']
        tokensWithBalance = []
        for token in tokens:
            if int(token['balance']) > 0:
                tokensWithBalance.append(token)
        return tokensWithBalance

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