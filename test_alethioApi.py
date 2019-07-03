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
    def test_getERC20Balance(self, resp):
        """Test getERC20Balance method alethioApi class. """
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
                    'balance': '3777310500000000000000'
            }]}
        assert self.api.getERC20Balances('0x1')[0]['symbol'] == 'GTRN'