from ens import ENS
from web3 import Web3
import requests
import argparse

parser = argparse.ArgumentParser(description="Learn about an ETH address")
parser.add_argument('--ens', help='An ENS address')
parser.add_argument('--provider', help='Your web3 provider', default='https://mainnet.infura.io')
args = parser.parse_args()

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io'))
ns = ENS.fromWeb3(w3)

eth_address = ns.address(args.ens)

print(eth_address)
r = requests.get(f'https://api.aleth.io/v1/accounts/{eth_address}')
print(w3.fromWei(int(r.json()['data']['attributes']['balance']),'ether'))