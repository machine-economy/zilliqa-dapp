# -*- coding: utf-8 -*-
# config.py
# Zilliqa dapp Project - Machine Economy
# Copyright (c) 2019  Well Bred Software Limited and Rustiq Technology Limited
# This code is licensed under the MIT license (see LICENSE for terms).

"""
config.py
zil_01 - configuration data - account keys, etc.
"""


class Config(object):
    #
    '''
    #  Default account definitions ...
    #  ... update this with your account details.
    #default_account_address = '123456789abcdef0123456789abcdef012345668'
    default_account_address = '[Add contract owner account address here]'
    keystore_file = 'data/accounts/test_account_1.json'
    keystore_passphrase = 'machine economy passphrase 0001'
    #
    #  Payee account definitions ...
    #  ... update this with your account details.
    #payee_account_address = 'zil123456789012345678901234567890123456789'
    #payee_account_address = '[Add payee account address here]'
    payee_keystore_file = 'data/accounts/test_account_2.json'
    payee_keystore_passphrase = 'machine economy passphrase 0002'
    #
    #
    #  Default contract defn ...
    #default_contract_address = '45dca9586598c8af78b191eaa28daf2b0a0b4f43'
    default_contract_address = None
    '''
    #
    # ******      Working Data       *****
    #
    default_account_address = 'b50b61ecb98683083ad80f45bde5d15ea5ab745b'
    keystore_file = 'data/accounts/test_0001_keystore.json'
    keystore_passphrase = 'test account 0001 passphrase'
    #
    #
    #  Payee account definitions ...
    #  ... update this with your account details.
    payee_account_address = 'zil1fftsz0t5lvdlhlhj4cal9xzva9cvulmz5tv7sx'
    payee_keystore_file = 'data/accounts/test_account_2.json'
    payee_keystore_passphrase = 'machine economy passphrase 0002'
    #
    #
    #  Default contract defn ...
    default_contract_address = None
    #default_contract_address = '45dca9586598c8af78b191eaa28daf2b0a0b4f43'
