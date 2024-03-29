import alethioApi
from datetime import datetime
from bullet import Bullet, Input   
 
def printEtherTransaction(trxn):
    """Print details of an Ethereum transaction in a CLI-friendly version. """
    print('Transaction Hash: ' + trxn['relationships']['transaction']['data']['id'])
    print('Amount: ' + api.normalizeValue('18',trxn['attributes']['total']))
    print('From: ' + trxn['relationships']['from']['data']['id'])
    print('To: ' + trxn['relationships']['to']['data']['id'])
    print('Transaction block creation time: ' + str(datetime.fromtimestamp(trxn['attributes']['blockCreationTime'])))


def printTokenTransaction(trxn):
    """Print details of a token transaction in a CLI-friendly version. """
    print('Transaction Hash: ' + trxn['relationships']['transaction']['data']['id'])
    if trxn['attributes']['symbol']: print('Symbol: ' + trxn['attributes']['symbol'])
    print('Amount: ' + api.normalizeValue(trxn['attributes']['decimals'],trxn['attributes']['value']))
    print('From: ' + trxn['relationships']['from']['data']['id'])
    print('To: ' + trxn['relationships']['to']['data']['id'])
    print('Transaction block creation time: ' + str(datetime.fromtimestamp(trxn['attributes']['blockCreationTime'])))

def printTransactionSummary(trxn):
    """Print transaction summary in a CLI-friendly version. """
    print('Transaction Hash: ' + trxn['id'])
    print('Amount: ' + api.normalizeValue('18',trxn['attributes']['value']))
    print('From: ' + trxn['relationships']['from']['data']['id'])
    print('To: ' + trxn['relationships']['to']['data']['id'])
    print('Transaction block creation time: ' + str(datetime.fromtimestamp(trxn['attributes']['blockCreationTime'])))
    if trxn['attributes']['msgPayload']:
        for key, value in trxn['attributes']['msgPayload'].items():
            if key in ['funcDefinition', 'funcName','funcSignature','funcSelector','inputs','outputs']:
                print(str(key) + ": " + str(value))

def printTransactionDetail(trxn):
    """Print every field in a transaction. """
    for key, value in trxn.items():
        if key == 'links':
            continue
        elif type(value) == dict:
            printTransactionDetail(value)
        else:
            print(str(key)+ ': ' + str(value))



print('Welcome to the Command-Line Ethereum Blockchain Explorer.')
cli = Bullet(prompt = 'Do you want to see raw API responses with each query?', choices = ['Yes','No'])
choice = cli.launch()
if choice == 'Yes':
    loggingLevel = 'INFO'
else: 
    loggingLevel = 'WARNING'

cli = Bullet(prompt = 'Do you wish to use your Alethio developer API key?', choices=['Yes','No'])
choice = cli.launch()

if choice == "Yes":
    cli = Input(prompt = "Enter API key: ")
    token = cli.launch()
else:
    token = ''

api = alethioApi.alethioAPI(loggingLevel=loggingLevel, token=token)

while 1:
    cli = Bullet(prompt = 'What do you want to explore?', choices=['address','transaction','quit'])
    choice = cli.launch()
    if choice == 'address':
        cli = Input(prompt = 'Enter address (either Ethereum address or ENS address): ', strip=True)
        address = cli.launch()
        try:
            ethAddress = api.validateAddress(address)
        except:
            print('Invalid address.  Please validate your address and try again.')
            continue
        cli = Bullet(prompt = 'Which address attribute do you want to see?', choices=['balance','token balances','ether transfers', 'token transfers', 'contract messages'])
        choice = cli.launch()
        if choice == 'balance':
            print('Ether balance: '+ str(api.getEthBalance(ethAddress)))
        if choice == 'token balances':
            choices = []
            for token in api.getTokenBalances(ethAddress):
                if token['symbol']:
                    print('Symbol: ' + token['symbol'] + ', Token: ' + token['name'] + ', Amount: ' + token['balance'])
                    choices.append(token['symbol'])
                else:
                    print('Contract: ' + token['contractAddress'] + ', Amount: ' + token['balance'])
                    choices.append(token['contractAddress'])
            cli = Bullet(prompt='See token transfers associated with wallet/token or main menu?', choices=['token transfers','main menu'])
            choice = cli.launch()
            if choice == 'token transfers':
                cli = Bullet(prompt = 'Select token from below:', choices=choices)
                choice = cli.launch()
                transfers = api.getTokenTransfers(ethAddress)
                for trxn in transfers['data']:
                    if trxn['attributes']['symbol'] == choice:
                        printTokenTransaction(trxn)
                    elif trxn['relationships']['token']['data']['id'] == choice:
                        printTokenTransaction(trxn)
            else:
                continue
        if choice == 'ether transfers':
            response = api.getEthTransfers(ethAddress)
            for trxn in response['data']:
                printEtherTransaction(trxn)
            choice = 'Yes'
            while choice == 'Yes':
                cli = Bullet(prompt = 'Do you want to see more transactions?', choices=['Yes','No'])
                choice = cli.launch()
                if choice == 'Yes':
                    try:
                        response = api.authRequest(api.token,response['links']['next']).json()
                        print(response)
                        for trxn in response['data']:
                            printEtherTransaction(trxn)
                    except:
                        "No more transactions available."
                        continue

        if choice == 'token transfers':
            response = api.getTokenTransfers(ethAddress)
            for trxn in response['data']:
                printTokenTransaction(trxn)
            choice = 'Yes'
            while choice == 'Yes':
                cli = Bullet(prompt = 'Do you want to see more transactions?', choices=['Yes','No'])
                choice = cli.launch()
                if choice == 'Yes':
                    try:
                        response = api.authRequest(api.token,response['links']['next']).json()
                        print(response)
                        for trxn in response['data']:
                            printEtherTransaction(trxn)
                    except:
                        "No more transactions available."
                        continue
        if choice == 'contract messages':
            cli = Bullet(prompt = 'Do you want to see all contract messages for this address or between this and another specific address?', choices=[
                    'All',
                    'Specific Address'])
            choice = cli.launch()
            if choice == 'Specific Address':
                cli = Input(prompt = 'Please provide the second address: ')
                toAddress = cli.launch()
                for trxn in api.getContractMessages(ethAddress,to=toAddress):
                    printTransactionSummary(trxn)
            else:
                choices = []
                response = api.getContractMessages(ethAddress)
                for trxn in response['data']:
                    choices.append(trxn['id'])
                    printTransactionSummary(trxn)
                if response['meta']['page']['hasNext'] == True:
                    choice = "More Transactions"
                else:
                    cli = Bullet(prompt = 'Do you want to see associated log entries for a message or return to main menu?', choices=[
                        'Log Entries',
                        'Main Menu'])
                    choice = cli.launch()
                while choice == "More Transactions":
                    cli = Bullet(prompt = 'Do you want to see more transactions, associated log entries, or return to main menu?', choices=[
                        'More Transactions',
                        'Log Entries',
                        'Main Menu'])
                    choice = cli.launch()
                    if choice == 'More Transactions':
                        try:
                            response = api.authRequest(api.token,response['links']['next']).json()
                            choices = []
                            for trxn in response['data']:
                                choices.append(trxn['id'])
                                printTransactionSummary(trxn)
                        except:
                            "No more transactions available."
                    if response['meta']['page']['hasNext'] == False:
                        cli = Bullet(prompt = 'Do you want to see associated log entries for a message or return to main menu?', choices=[
                            'Log Entries',
                            'Main Menu'])
                        choice = cli.launch()
                if choice == "Log Entries":
                    cli = Bullet(prompt='Select message ID to see log entries associated with this message: ', choices=choices)
                    choice = cli.launch()
                    response = api.getLogEntriesForContractMessage(choice)
                    for entry in response['data']:
                        printTransactionDetail(entry)
                else:
                    continue
    elif choice == 'transaction':
        cli = Input(prompt = "Enter transaction hash: ")
        trxnHash = cli.launch()
        trxn = api.getTransactionDetails(trxnHash)
        cli = Bullet(prompt = "Print transaction summary or details?", choices = ['Summary','Details'])
        choice = cli.launch()
        if choice == 'Summary':
            printTransactionSummary(trxn['data'])
        else:
            printTransactionDetail(trxn['data'])
    elif choice == 'quit':
        break


        