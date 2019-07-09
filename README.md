# Command-Line Interactive Ethereum Explorer

Leverage the Alethio API to explore the Ethereum blockchain from the command Line

## Features

* Supports ENS address lookup/conversion to Ethereum addresses
* View ether/token balances for any given address
* View ether/token transfers associated with any given Ethereum address
* View smart contract messages associated with a given Ethereum address
* Look up any transaction by its transaction hash and see transaction summary/details 
* View all smart contract messages between any two Ethereum addresses

## Usage

* Run the explorer - `python interactive-explorer.py`
* Provide an Alethio developer key if applicable
* Provide an Ethereum address/ENS address/transaction hash
* Follow prompts and explore the blockchain!

## Example Use Cases

* See account's ERC-20 token balance and then see all token transfers associated 
  with that account and token
  ** Enter Ethereum address
  ** Select Token balances
  ** Select Token transfers
  ** Select token from drop-down to see associated token transfers
  ** Copy transaction hash and then look up specific transaction details based on hash
* See all contract messages between a given Ethereum account and a Uniswap exchange contract
  ** Enter Ethereum address
  ** Select contract messages
  ** Select option to see messages exchanged with specific address
  ** Enter Uniswap exchange address
  ** Peruse message list

# Alethio API Wrapper/Client Library

This is a python wrapper for the Alethio API that provides access to most
major features of the Alethio API.  The [API documentation](https://api.aleth.io/v1/docs)
explains the details of each individual field and message type so please refer to those links for details.

## API messages

* getEthBalance - provides Ethereum balance
* getTokenBalances - provides all token balances associated with a given Ethereum address.  All values
  are normalized to Ethereum-style notation
* getEthTransfers - provides a paginated list of all of Ether transfers associated with a given 
  Ethereum address
* getTokenTransfers - provides a paginated list of token transfers associated with a given Ethereum 
  address
* getContractMessages - provides a paginated list of contract messages associated with a a given 
  Ethereum address.
* getLogEntriesForContractMessage - provides all log entries associated with a given contract messaage
* getTransactionDetails - provides all data elements associated with a given transaction hash

## Helper functions

* normalizeValue - converts a token value based on the # decimals the token uses in notation (similar to web3.fromWei)
* authRequest - creates an HTTP GET request that conforms to Alethio API authentication requirements and returns a standard 
  [Python Requests](https://2.python-requests.org/en/master/) response object
* ENStoEthAddress - resolves an ENS address to a standard Ethereum address
* validateAddress - validates that a provided address conforms to Ethereum address naming standards

## Roadmap

* Add additional messages for additional endpoints (e.g. blocks, tokens)
* Add additional control over pagination of results returned for Ether-Transfers and Token-Transfers
