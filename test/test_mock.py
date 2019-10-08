# Zilliqa dapp Project - Machine Economy
# Copyright (c) 2019  Well Bred Software Limited and Rustiq Technology Limited
# This code is licensed under the MIT license (see LICENSE for terms).

#  Fix-up the path to the 'root' directory ...
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import logging
from pyzil.account import Account
from pyzil.zilliqa.chain import BlockChain
from pyzil.zilliqa.units import Qa, Zil

from mock.src.getAccounts import accountPrivateKeys
from src import zil_01

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# Interface to the local Kaya instance.
mockNet = BlockChain("http://localhost:4200/", version = 1, network_id = 111)

# Test the mock accounts.
def test_mock_accounts():
    # There are 10 initial accounts by default.
    assert len(accountPrivateKeys) == 10
    for adr in accountPrivateKeys:
        # Every account number is a 20-byte hex string.
        assert len(adr) == 40
        accn = int(adr, 16)
        # Every secret key is a 32-byte hex string.
        key = accountPrivateKeys[adr]
        assert len(key) == 64
        keyn = int(key, 16)

# Test the account API and the initial balances.
def test_initial_balances():
    for adr in accountPrivateKeys:
        account = Account(address = adr, private_key = accountPrivateKeys[adr])
        zil = zil_01.Zil_01(net = mockNet, account = account)
        # Check we have an object.
        assert zil is not None
        # Check the account field is set.
        assert zil.account == account
        # Check the initial balance.
        assert zil.get_balance() == Qa(10 ** 18).toZil()
