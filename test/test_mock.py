# Zilliqa dapp Project - Machine Economy
# Copyright (c) 2019  Well Bred Software Limited and Rustiq Technology Limited
# This code is licensed under the MIT license (see LICENSE for terms).

import pytest
import logging
from mock.src.getAccounts import accountPrivateKeys

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# Test the mock accounts.
def test_mock_accounts():
    # There are 10 initial accounts by default.
    assert len(accountPrivateKeys) is 10
    for acc in accountPrivateKeys:
        # Every account number is a 20-byte hex string.
        assert len(acc) is 40
        accn = int(acc, 16)
        # Every secret key is a 32-byte hex string.
        key = accountPrivateKeys[acc]
        assert len(key) is 64
        keyn = int(key, 16)
