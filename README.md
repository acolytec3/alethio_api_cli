# Command-Line Ethereum Explorer

Leverage the Alethio API to explore the Ethereum blockchain from the command Line

## Command Line Interface Usage

`python row.py [args]`

### CLI arguments

* `--address "0x1234..."` or `"alice.eth"` -- Look up the details of an Ethereum address 
* `--provider "https://my.ethereumprovider.com"` -- Specify an Web3 HTTP Provider (defaults to Infura)
* `--balance, -b` -- Print Ether balance associated with provided address
* `--tokens, -t` -- Print token balances associated with provided address
* `--ethTransfers, -et` -- Print Ether transfers associated with provided address
* `--tokenTransfers, -tt` -- Print token transfers associated with provided address
* `--contractMessages, -cm` -- Print smart contract interactions associated with provided address
* `--logLevel, -ll` -- Set logging level (i.e. DEBUG, INFO, WARNING, etc)

## Interactive Explorer Usage

`python interactive-explorer.py`

## Roadmap

* Build out Uniswap transaction history
