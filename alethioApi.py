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
        logging.info(response.json())
        return response.json()

    def getTokenTransfers(self, ethAddress):
        """Get Ether transfers associated with current address. """
        ethAddress = self.validateAddress(ethAddress)
        response = self.authRequest(self.token,f'https://api.aleth.io/v1/accounts/{ethAddress}/tokenTransfers')
        logging.info(response.json())
        return response.json()

    def getContractMessages(self, ethAddress, to=None):
        """Get Smart Contract messages associated with current address. """
        ethAddress = self.validateAddress(ethAddress)

        # Only return contract messages between ethAddress and toAddress
        if to:  
            toAddress = self.validateAddress(to)
            response = self.authRequest(self.token,f'https://api.aleth.io/v1/contract-messages?filter[account]={ethAddress}').json()
            messages = []
            for message in response['data']:
                if (message['relationships']['from']['data']['id'] == toAddress) or (message['relationships']['originator']['data']['id'] == toAddress):
                    messages.append(message)
            while response['meta']['page']['hasNext'] == True:
                response = self.authRequest(self.token,response['links']['next']).json()
                for message in response['data']:
                    logging.info(message)
                    if (message['relationships']['from']['data']['id'] == toAddress) or (message['relationships']['originator']['data']['id'] == toAddress):
                        messages.append(message)
            return messages            
        
        # Return all contract messages where ethAddress is originator or receiver of message
        response = self.authRequest(self.token,f'https://api.aleth.io/v1/contract-messages?filter[account]={ethAddress}')
        logging.info(response.json())
        return response.json()
    
    def getTransactionDetails(self, trxnHash):
        """"Get transaction details associated with a given transaction hash. """
        response = self.authRequest(self.token, 'https://api.aleth.io/v1/transactions/' + trxnHash)
        logging.info(response.json())
        return response.json()

    def getLogEntriesForContractMessage(self, contractMsgID):
        """"Get log entries produced by executing a given contract message. """
        response = self.authRequest(self.token, f'https://api.aleth.io/v1/contract-messages/{contractMsgID}/logEntries')
        logging.info(response.json())
        return response.json()

    def normalizeValue(self, decimals, value):
        """Convert a value from a Web3 transaction to an Ether equivalent value and return as a string. """
        return str(int(value) / 10**int(decimals))
    
    def authRequest(self, token, request):
        """Make GET request to Alethio API using authentication. """
        logging.info('Request sent to Alethio: ' + request)
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

