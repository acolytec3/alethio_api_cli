from prompt_toolkit import prompt
from prompt_toolkit import validation
from prompt_toolkit import PromptSession
import alethioApi

api = alethioApi.alethioAPI(loggingLevel='INFO', token='')

session = PromptSession()

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


def printTokenTransaction(trxn):
    """Print details of a token transaction in a CLI-friendly version. """
    print('Transaction Hash: ' + trxn['relationships']['transaction']['data']['id'])
    print('Symbol: ' + trxn['attributes']['symbol'])
    print('Amount: ' + api.normalizeValue(trxn['attributes']['decimals'],trxn['attributes']['value']))
    print('From: ' + trxn['relationships']['from']['data']['id'])
    print('To: ' + trxn['relationships']['to']['data']['id'])

def printTransactionSummary(trxn):
    """Print transaction summary in a CLI-friendly version. """
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
    
while 1:
    choice = session.prompt('(a)ddress, (t)ransaction hash, (q)uit: ')
    if choice == 'a':
        ethAddress = session.prompt('Enter address: ')
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
                        print('Amount: ' + str(api.w3.fromWei(int(trxn['attributes']['value']),'ether')) + ' Token: ' + trxn['attributes']['symbol'])
                    elif trxn['relationships']['token']['data']['id'] == choice:
                        print('Contract: ' + token['contractAddress'] + ', Amount: ' + token['balance'])
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


        