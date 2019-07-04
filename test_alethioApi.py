import unittest
from unittest.mock import patch
import pytest
from alethioApi import alethioAPI
from decimal import Decimal

class testAlethioApi(unittest.TestCase):
    api = alethioAPI('')

    @patch('alethioApi.requests.get', resp = 1)
    def test_getEthBalance(self, resp):
        """Test getEthBalance method of alethioApi class. """
        resp.return_value.json.return_value = {'data':{'attributes':{'balance':'1000000000000000000'}}}
        assert self.api.getEthBalance('0x1') == Decimal('1')
        

    @patch('alethioApi.requests.get')
    def test_getTokenBalances(self, resp):
        """Test getTokenBalances method of alethioApi class. """
        resp.return_value.json.return_value = {'result':[
            {
                'symbol': 'GTRN', 
                'name': 'GitTron', 
                'decimals': '', 
                'contractAddress': '0x162d3e80d51f96240ae0a44ab3a5b1ea23920ce4', 
                'balance': '5'
                }, 
                {
                    'symbol': 'ODHAV', 
                    'name': 'OdhavToken', 
                    'decimals': '18', 
                    'contractAddress': '0x30b8d24688991f0f0e6270913182c97a533a85fb', 
                    'balance': '0'
            }]}
        tokens = self.api.getTokenBalances('0x1')
        assert tokens[0]['symbol'] == 'GTRN'
        with self.assertRaises(IndexError):
            tokens[1]

    @patch('alethioApi.requests.get')
    def test_getEthTransactions(self, resp):
        """Test getEthTransactions method of alethioApi class. """
        resp.return_value.json.return_value = {
            'data': [{
                'type': 'EtherTransfer',
                'id': '0x0079c69c004e00004200f7f0b0a20179',
                'attributes': {
                    'transferType': 'ContractMessageTransfer',
                    'value': '4287663873500000512',
                    'fee': '0',
                    'total': '4287663873500000512',
                    'blockCreationTime': 1560839506,
                    'globalRank': [],
                    'cursor': '0x0079c69c004e00004200f7f0b0a20179'
                }
            }]
        }
        assert self.api.getEthTransfers('0x1')[0]['attributes']['value'] == '4287663873500000512'

    @patch('alethioApi.requests.get')
    def test_gettokenTransactions(self, resp):
        """Test getTokenTransactions method of alethioApi class. """
        resp.return_value.json.return_value = {
            'data':[{
                'type': 'TokenTransfer',
                 'id': '0x0078c0b100a6000081019853a8374aa3',
                 'attributes': {
                     'blockCreationTime': 1559932370, 
                     'cursor': '0x0078c0b100a6000081019853a8374aa3', 
                     'decimals': 18,
                     'globalRank': [7913649, 166, 0], 
                     'symbol': 'VTY', 
                     'value': '2395143740436544241664'
                     }
            }]
        }
        assert self.api.getTokenTransfers('0x1')[0]['attributes']['symbol'] == 'VTY'