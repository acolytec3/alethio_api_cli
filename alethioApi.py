from ens import ENS
from web3 import Web3
import requests
import logging
import sys


class alethioAPI:
    """Alethio API wrapper."""

    def __init__(self, provider="https://mainnet.infura.io", loggingLevel='WARNING', token=''):
        """ Initialize instance of alethioAPI. """
        self.w3 = Web3(Web3.HTTPProvider(provider))
        logging.basicConfig(stream=sys.stdout, level=logging.getLevelName(loggingLevel))
        self.token = token
    
    def getEthBalance(self, ethAddress):
        """ Get Ether Balance for current address."""
        ethAddress = self.validateAddress(ethAddress)
        response = self.authRequest(self.token, f'https://api.aleth.io/v1/accounts/{ethAddress}')
        logging.info(response.json())
        return self.w3.fromWei(int(response.json()['data']['attributes']['balance']),'ether')

    def getTokenBalances(self, ethAddress):
        """ Get token balances for current address. Note: This function does not return tokens with a zero balance. """
        ethAddress = self.validateAddress(ethAddress)
        response = requests.get('https://blockscout.com/eth/mainnet/api?module=account&action=tokenlist&address='+ethAddress)
        logging.info(response.json())
        if response.json()['status'] != '1':
            raise Exception('API returned unexpected response')
        tokens = response.json()['result']
        tokensWithBalance = []
        for token in tokens:
            if token['decimals']:
                token['balance'] = self.normalizeValue(token['decimals'],token['balance'])
            tokensWithBalance.append(token)
        return tokensWithBalance

    def getEthTransfers(self, ethAddress):
        """Get Ether transfers associated with current address. """
        ethAddress = self.validateAddress(ethAddress)
        response = self.authRequest(self.token,f'https://api.aleth.io/v1/accounts/{ethAddress}/etherTransfers')
        logging.info(response.json()['data'])
        return response.json()['data']

    def getTokenTransfers(self, ethAddress):
        """Get Ether transfers associated with current address. """
        ethAddress = self.validateAddress(ethAddress)
        response = self.authRequest(self.token,f'https://api.aleth.io/v1/accounts/{ethAddress}/tokenTransfers')
        logging.info(response.json()['data'])
        return response.json()['data']

    def getContractMessages(self, ethAddress):
        """Get Smart Contract messages associated with current address. """
        ethAddress = self.validateAddress(ethAddress)
        response = self.authRequest(self.token,f'https://api.aleth.io/v1/contract-messages?filter[account]={ethAddress}')
        logging.info(response.json()['data'])
        return response.json()['data']
    
    def getTransactionDetails(self, trxnHash):
        """"Get transaction details associated with a given transaction hash. """
        response = self.authRequest(self.token, 'https://api.aleth.io/v1/transactions/' + trxnHash)
        logging.info(response.json()['data'])
        return response.json()['data']

    def normalizeValue(self, decimals, value):
        """Convert a value from a Web3 transaction to an Ether equivalent value and return as a string. """
        return str(int(value) / 10**int(decimals))
    
    def authRequest(self, token, request):
        """Make GET request to Alethio API using authentication. """
        return requests.get(request, auth=(token,''))

    def validateAddress(self, address):
        """ Check address and convert to Eth address if ENS address. """
        if address.find('.eth') != -1:
            return self.ENStoEthAddress(address)
        elif address[0:2] == '0x':
            return address
        else:
            raise Exception('Invalid address.  Please provide an ENS address or standard Ethereum address')
            
    def ENStoEthAddress(self, ens):
        """ Convert ENS address to standard Ethereum address. """
        if self.w3.isConnected():
            ns = ENS.fromWeb3(self.w3)
            address = ns.address(ens)
            if address != None:
                return address
            else:
                raise Exception('Address cannot be resolved.')
        else:
            raise Exception('Web3 not connected.')

    def ethToENS(self, ethAddress):
        """ Convert Ethereum address to ENS address (if available). """
        if self.w3.isConnected():
            ns = ENS.fromWeb3(self.w3)
            ens = ns.reverse(ethAddress)
            if ens != None:
                return ens
            else:
                return ethAddress
        else:
            raise Exception('Web3 not connected.')