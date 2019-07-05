from prompt_toolkit import prompt
from prompt_toolkit import validation
from prompt_toolkit import PromptSession
import alethioApi

api = alethioApi.alethioAPI(loggingLevel='INFO', token='')

session = PromptSession()

def trxnDetails():
    """Print transaction details for given transaction. """
    trxnHash = session.prompt('Enter transaction hash: ')
    print('Transaction details: ' + str(api.getTransactionDetails(trxnHash)['attributes']['msgPayload']['funcName']))
 

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
                print('Amount: ' + trxn['attributes']['total'])
        if choice == 'to':
            for trxn in api.getTokenTransfers(ethAddress):
                print('Amount: ' + str(api.w3.fromWei(int(trxn['attributes']['value']),'ether')) + ' Token: ' + trxn['attributes']['symbol'])
    elif choice == 't':
        trxnDetails()
    elif choice == 'q':
        break


        