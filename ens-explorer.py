from ens import ENS
from web3 import Web3
import requests
import argparse

parser = argparse.ArgumentParser(description="Learn about an ETH address")
parser.add_argument('--ens', '-e', help='An human readable Ethereum address with a .eth extension')
parser.add_argument('--address', '-a', help='An Ethereum address of the form 0x1a2b3c...')
parser.add_argument('--provider', help='A preferred web3 provider for interacting with the blockchain; defaults to infura mainnet', default='https://mainnet.infura.io')
args = parser.parse_args()

w3 = Web3(Web3.HTTPProvider(args.provider))
if args.ens:
    ns = ENS.fromWeb3(w3)
    eth_address = ns.address(args.ens)
if args.address:
    eth_address = args.address

r = requests.get(f'https://api.aleth.io/v1/accounts/{eth_address}')
print(w3.fromWei(int(r.json()['data']['attributes']['balance']),'ether'))