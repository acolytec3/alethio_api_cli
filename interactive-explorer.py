from prompt_toolkit import prompt
from prompt_toolkit import validation
from prompt_toolkit import PromptSession
import alethioApi

api = alethioApi.alethioAPI(loggingLevel='INFO', token='')

session = PromptSession()

while 1:
    choice = session.prompt('(a)ddress, (t)ransaction hash, (q)uit: ')
    if choice == 'a':
        ethAddress = session.prompt('Enter address: ')
    if choice == 't':
        trxnHash = session.prompt('Enter transaction hash: ')
    if choice == 'q':
        break
    choice = session.prompt('(b)alance, (t)oken balances, (e)ther transfers, (to)ken transfers')
    if choice == 'b':
        print('Ether balance: '+ str(api.getEthBalance(ethAddress)))
    if choice == 't':
        for token in api.getTokenBalances(ethAddress):
            if token['symbol']:
                print('Symbol: ' + token['symbol'] + ', Token: ' + token['name'] + ', Amount: ' + token['balance'])
            else:
                print('Contract: ' + token['contractAddress'] + ', Amount: ' + token['balance'])
    if choice == 'e':
        for trxn in api.getEthTransfers(ethAddress):
            print('Amount: ' + trxn['attributes']['total'])
    if choice == 'to':
        for trxn in api.getTokenTransfers(ethAddress):
            print('Amount: ' + str(api.w3.fromWei(int(trxn['attributes']['value']),'ether')) + ' Token: ' + trxn['attributes']['symbol'])


        