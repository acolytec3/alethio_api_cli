import unittest
from unittest.mock import patch
import pytest
from alethioApi import alethioAPI
from decimal import Decimal

class testAlethioApi(unittest.TestCase):
    api = alethioAPI('')
    @patch('alethioApi.alethioAPI.ENStoEthAddress', ens = 1)
    @patch('alethioApi.requests.get', resp = 1)
    def test_getEthBalance(self, resp, ens):
        """Test getEthBalance method of alethioApi class. """
        resp.return_value.json.return_value = {'data':{'attributes':{'balance':'1000000000000000000'}}}
        assert self.api.getEthBalance('0x1') == Decimal('1')
        
    @patch('alethioApi.alethioAPI.ENStoEthAddress', ens = 1)
    @patch('alethioApi.requests.get')
    def test_getTokenBalances(self, resp, ens):
        """Test getTokenBalances method of alethioApi class. """
        resp.return_value.json.return_value = {
                'status': '1',
                'result':[
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

    @patch('alethioApi.alethioAPI.ENStoEthAddress', ens = 1)
    @patch('alethioApi.requests.get')
    def test_getEthTransactions(self, resp, ens):
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

    @patch('alethioApi.alethioAPI.ENStoEthAddress', ens = 1)
    @patch('alethioApi.requests.get')
    def test_gettokenTransactions(self, resp, ens):
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

    @patch('alethioApi.alethioAPI.ENStoEthAddress', ens = 1)
    @patch('alethioApi.requests.get')
    def test_getContractMessages(self, resp, ens):
        """Test getContractMessages method of alethioApi class. """
        resp.return_value.json.return_value = {
            'data':[{
                'type': 'ContractMessage',
                 'id': 'msg:0x557dc410ce83b3d1f5e7e0129f89b3db53d1180ad279c02aa8c3f2aee0a7f35e:2', 
                 'attributes': {
                     'blockCreationTime': 1558517007, 
                     'cmsgIndex': 2,
                     'cursor': '0x0077271a00ef00002001036ad7427ebe', 
                     'fee': '0', 
                     'globalRank': [7808794, 239, 0], 
                     'msgCallDepth': 1, 
                     'msgError': False, 
                     'msgErrorString': '', 
                     'msgGasLimit': '2300', 
                     'msgGasUsed': 0, 
                     'msgPayload': {
                         'funcName': '', 
                         'funcSelector': '', 
                         'funcSignature': '', 
                         'funcDefinition': '', 
                         'inputs': [], 
                         'outputs': [], 
                         'raw': ''
                         },
                    'msgType': 'ValueContractMsg',
                    'txGasPrice': '11000000000', 
                    'value': '8000000000000000'
                    }
            }
        ]}
        assert self.api.getContractMessages('0x1')[0]['type'] == 'ContractMessage'
        assert self.api.getContractMessages('0x1')[0]['attributes']['msgType'] == 'ValueContractMsg'

    @patch('alethioApi.requests.get')
    def test_getTransactionDetails(self, resp):
        """Test getTransactionDetails method of alethioApi class. """
        resp.return_value.json.return_value = {
            'data':{
                'type': 'Transaction', 
                'id': '0xfcf03c816ac2f916f14fda251218043e3bfe66ecf72aeaf5140f0e1f5e86fba3', 
                'attributes': {
                    'blockCreationTime': 1556286879,
                    'cursor': '0x0074a0f10033000010009b00bbc20f19', 
                    'fee': '1388940000000000', 
                    'firstSeen': 1556286847, 
                    'globalRank': [7643377, 51, 0], 
                    'msgError': False, 
                    'msgErrorString': '', 
                    'msgGasLimit': '250000', 
                    'msgPayload': {
                        'funcName': 'transfer', 
                        'funcSelector': '0xa9059cbb', 
                        'funcSignature': 'transfer(address,uint256)', 
                        'funcDefinition': 'transfer(address to, uint256 value) public nonpayable returns (bool param0)', 
                    }
                }
            }
        }
        assert self.api.getTransactionDetails('0x1')['type'] == 'Transaction'