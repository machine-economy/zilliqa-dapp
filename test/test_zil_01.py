# -*- coding: utf-8 -*-
# test_zil_01.py
# Zilliqa dapp Project - Machine Economy
# Copyright (c) 2019  Well Bred Software Limited and Rustiq Technology Limited
# This code is licensed under the MIT license (see LICENSE for terms).

"""
test_zil_01.py
test_zil_01 module - Zilliqa machine economy zil_01 module tests - 
Performs basic tests on the zil_01 module.
"""

__TOOL = "test_zil_01.py"
__VERSION = "0.2.6-b36"
__DESC = ""


"""
[***  To be removed ***]
[Add notes on the expected class interface.]

class: Zil_01()
  instance vars:
    account; contract; ...
  methods:
    load_contract(contract_address)
    get_...(p1, p2, ...)

"""


#  Fix-up the path to the 'root' directory ...
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import logging

import time
from src import zil_01
from pyzil.account import Account
from pyzil.contract import Contract
from pyzil.zilliqa.chain import active_chain


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


class TestZil_01:
    def test_Zil_01(self):
        pass


#  Global data across tests ...  [** This needs reviewed **]
zil = None
account = None
account_address = None


def test_1_Zil_01():
    global zil
    global account
    if account_address:
        #  Use the address for the account ...
        account = Account(address=account_address)
    else:
        #  Get account from keystore data ...
        keystore_file = "data/accounts/test_account_1.json"
        keystore_pwd = "test account 0001 passphrase"
        account = Account.from_keystore(keystore_pwd, keystore_file)
    print("Account:", account)
    #  Create the Zil object ...
    zil = zil_01.Zil_01(account=account)
    #  Check we have an object ...
    assert zil is not None
    #  Check object has docstring...
    assert zil.__doc__ is not None
    #  Check the account field is set...
    assert zil.account == account


#   Test the compile and deploy contract method ...
#@pytest.mark.deploytest
@pytest.mark.skip(reason="Deploy not executed by default")
def test_deploy_contract():
    #  Get the code filename ...
    sc_code_file = "src/zil_01_hello.scilla"
    #  Compile and deploy the contract ...
    zil.compile_contract(sc_code_file, account=account)
    receipt = zil.contract.last_receipt
    assert receipt['success'] is True
    assert zil.contract.status == Contract.Status.Deployed


def test_load_contract():
    """Test the contract gets loaded.  Currently uses last loaded contract."""
    #  Set the contract to be the last deployed one ...
    owner_addr = account.address
    contracts = Contract.get_contracts(owner_addr)
    contract_addr = contracts[-1].address
    #if hard_coded_addr:
    #    address = "45dca9586598c8af78b191eaa28daf2b0a0b4f43"
    zil.load_contract(address=contract_addr)
    #
    #  Check the contract field is set...
    assert zil.contract


'''
#  *****  Move this to separate test file for HelloWorld contract  *****
def test_resetHello():
    #  [TBC] Set params and call the contract setHello function ...
    gas_factor = 1
    my_gas_price = int(active_chain.api.GetMinimumGasPrice()) * gas_factor
    #my_gas_limit = 100000 * gas_factor
    my_gas_limit = 10000
    print(f"resetHello():  my_gas_limit: {my_gas_limit}    "
          "my_gas_price: {my_gas_price}")
    #  Call the resetHello function ...
    zil.contract.call(method="resetHello",
                             gas_price=my_gas_price,
                             gas_limit=my_gas_limit,
                             params=[])
    assert zil.contract.last_receipt
    receipt = zil.contract.last_receipt
    #print(f"receipt:  {receipt}")
    assert receipt['success'] is True


def test_getHello(gas_factor=1):
    #  Get the getHello function ...
    my_gas_price = int(active_chain.api.GetMinimumGasPrice()) * gas_factor
    my_gas_limit = 10000
    print(f"getHello():  my_gas_limit: {my_gas_limit}    "
          "my_gas_price: {my_gas_price}")
    resp = zil.contract.call(method="getHello",
                             gas_price=my_gas_price,
                             gas_limit=my_gas_limit,
                             params=[])
    print("\nlast_receipt: ...")
    print(zil.contract.last_receipt)
    assert zil.contract.last_receipt
    receipt = zil.contract.last_receipt
    print(f"receipt:  {receipt}")
    assert receipt['success'] is True
    if receipt['success'] is not True:
        print(f"** Result (success): {receipt['success']}")
    event_logs = receipt['event_logs']
    print(f"event_logs:  {event_logs}")
    params = event_logs[0]['params']
    #print(f"params:  {params}")
    params0 = params[0]
    #print(f"params0:   vname: {params0['vname']}  type: {params0['type']}  "
    #      "value: {params0['value']}")
    msg = params0['value']
    print(f"--> Response msg: {msg}")
    assert msg == "[HelloWorld-Welcome]12345"
    print("\nresp: ...")
    print(resp)


def test_setHello(gas_factor=1):
    #  Set params and call the contract setHello function ...
    #
    #  Set up the call parameter(s):
    #  - A set of value_dicts, each containing:  name, type, value
    my_gas_price = int(active_chain.api.GetMinimumGasPrice()) * gas_factor
    my_gas_limit = 10000
    params = [Contract.value_dict("msg", "String",
                                  f"hi contract. ({time.ctime()}) [IFS1]")]
    zil.contract.call(method="setHello",
                             gas_price=my_gas_price,
                             gas_limit=my_gas_limit,
                             params=params)
    print(zil.contract.last_receipt)
    receipt = zil.contract.last_receipt
    assert receipt['success'] is True
'''


@pytest.mark.skip(reason="Not currently supported")
def test_show_info():
    #  Get the contract info ...
    pass
    """
    #  Turn this into a proper test ...
    zil.show_contract_info()
    #assert ...
    """


@pytest.mark.skip(reason="Not currently supported")
def test_helloWorld():
    """Test function for the helloWorld SC"""
    global zil
    #account = Account.from_keystore("zxcvbnm,", "m1_test1_keys.json")
    #print("Account:", account)
    #zil = zil_01.Zil_01(account=account)

    #  Get the contracts for this user's address ...


if __name__ == '__main__':
    print("%s (%s-%s)" % (__TOOL, __VERSION, __DESC))

    #test_Zil_01()
    #test_helloWorld()


"""
    resp = contract.call(method="getHello", params=[])
    print("\nresp: ...")
    pprint(resp)
    print("\nlast_receipt: ...")
    pprint(contract.last_receipt)

    print(f"... setHello:  {time.ctime()} ...")
    resp = contract.call(method="setHello",
                         params=[Contract.value_dict("msg", "String",
                         f"hi contract. ({time.ctime()}) [IFS1]")])
    pprint(resp)
    pprint(contract.last_receipt)

    print(f"... getHello [2]:  {time.ctime()} ...")
    resp = contract.call(method="getHello", params=[])
    print("resp:")
    pprint(resp)
    print("last_receipt:")
    pprint(contract.last_receipt)
"""
