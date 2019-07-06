from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator
from prompt_toolkit import PromptSession
import alethioApi


def trxnDetails():
    """Print transaction details for given transaction. """
    trxnHash = session.prompt('Enter transaction hash: ')
    trxn = api.getTransactionDetails(trxnHash)
    print('Transaction Hash: ' + trxn['id'])
    print('Amount: ' + api.normalizeValue('18',trxn['attributes']['value']))
    if trxn['attributes']['txGasUsed']: print('Gas used: ' + api.normalizeValue('18',trxn['attributes']['txGasUsed']))
    if trxn['attributes']['txGasUsed']: print('Fee: ' + api.normalizeValue('18',trxn['attributes']['txGasUsed']))
    print('From: ' + trxn['relationships']['from']['data']['id'])
    print('To: ' + trxn['relationships']['to']['data']['id'])
    if trxn['attributes']['msgPayload']:
        for key, value in trxn['attributes']['msgPayload'].items():
            if key in ['funcDefinition', 'funcName','funcSignature','funcSelector','inputs','outputs']:
                print(str(key) + ": " + str(value))
 
def printEtherTransaction(trxn):
    """Print details of an Ethereum transaction in a CLI-friendly version. """
    print('Transaction Hash: ' + trxn['relationships']['transaction']['data']['id'])
    print('Amount: ' + api.normalizeValue('18',trxn['attributes']['total']))
    print('From: ' + trxn['relationships']['from']['data']['id'])
    print('To: ' + trxn['relationships']['to']['data']['id'])
    print('Transaction block creation time: ' + trxn['attributes']['blockCreationTime'])


def printTokenTransaction(trxn):
    """Print details of a token transaction in a CLI-friendly version. """
    print('Transaction Hash: ' + trxn['relationships']['transaction']['data']['id'])
    if trxn['attributes']['symbol']: print('Symbol: ' + trxn['attributes']['symbol'])
    print('Amount: ' + api.normalizeValue(trxn['attributes']['decimals'],trxn['attributes']['value']))
    print('From: ' + trxn['relationships']['from']['data']['id'])
    print('To: ' + trxn['relationships']['to']['data']['id'])
    print('Transaction block creation time: ' + trxn['attributes']['blockCreationTime'])

def printTransactionSummary(trxn):
    """Print transaction summary in a CLI-friendly version. """
    print('Transaction Hash: ' + trxn['id'])
    print('Amount: ' + api.normalizeValue('18',trxn['attributes']['value']))
    if trxn['attributes']['txGasUsed']: print('Gas used: ' + api.normalizeValue('18',trxn['attributes']['txGasUsed']))
    if trxn['attributes']['txGasUsed']: print('Fee: ' + api.normalizeValue('18',trxn['attributes']['txGasUsed']))
    print('From: ' + trxn['relationships']['from']['data']['id'])
    print('To: ' + trxn['relationships']['to']['data']['id'])
    print('Transaction block creation time: ' + trxn['attributes']['blockCreationTime'])
    if trxn['attributes']['msgPayload']:
        for key, value in trxn['attributes']['msgPayload'].items():
            if key in ['funcDefinition', 'funcName','funcSignature','funcSelector','inputs','outputs']:
                print(str(key) + ": " + str(value))


api = alethioApi.alethioAPI(loggingLevel='INFO', token='')

session = PromptSession()

while 1:
    choice = session.prompt('(a)ddress, (t)ransaction hash, (q)uit: ')
    if choice == 'a':
        address = session.prompt('Enter address: ')
        try:
            ethAddress = api.validateAddress(address)
        except:
            print('Invalid address.  Please validate your address and try again.')
            continue
        choice = session.prompt('(b)alance, (t)oken balances, (e)ther transfers, (to)ken transfers: ')
        if choice == 'b':
            print('Ether balance: '+ str(api.getEthBalance(ethAddress)))
        if choice == 't':
            for token in api.getTokenBalances(ethAddress):
                if token['symbol']:
                    print('Symbol: ' + token['symbol'] + ', Token: ' + token['name'] + ', Amount: ' + token['balance'])
                else:
                    print('Contract: ' + token['contractAddress'] + ', Amount: ' + token['balance'])
            choice = session.prompt('(s)ee token transfers associated with specific token or (m)ain menu? ')
            if choice == 's':
                choice = session.prompt('Please enter the symbol or token address you want to see transfers for: ')
                transfers = api.getTokenTransfers(ethAddress)
                for trxn in transfers:
                    if trxn['attributes']['symbol'] == choice:
                        printTokenTransaction(trxn)
                    elif trxn['relationships']['token']['data']['id'] == choice:
                        printTokenTransaction(trxn)
        if choice == 'e':
            for trxn in api.getEthTransfers(ethAddress):
                printEtherTransaction(trxn)
        if choice == 'to':
            for trxn in api.getTokenTransfers(ethAddress):
                printTokenTransaction(trxn)
    elif choice == 't':
        trxnDetails()
    elif choice == 'q':
        break


        