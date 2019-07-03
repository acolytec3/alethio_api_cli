import unittest
from unittest.mock import patch
import pytest
from alethioApi import alethioAPI
from decimal import Decimal

class testAlethioApi(unittest.TestCase):
    @patch('alethioApi.requests.get', resp = 1)
    def test_getEthBalance(self, resp):
        """Test getEthBalance method of alethioApi class. """
        api = alethioAPI('')
        resp.return_value.json.return_value = {'data':{'attributes':{'balance':'1000000000000000000'}}}
        assert api.getEthBalance('0x1') == Decimal('1')
        


    def test_getERC20Balance(self):
        """Test getERC20Balance method alethioApi class. """
        pass