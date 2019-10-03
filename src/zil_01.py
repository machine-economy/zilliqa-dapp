#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# zil_01.py
# Zilliqa dapp Project - Machine Economy
# Copyright (c) 2019  Well Bred Software Limited and Rustiq Technology Limited
# This code is licensed under the MIT license (see LICENSE for terms).

"""
zil_01.py
zil_01 module - Zilliqa account/contract support - supports operations using
pyzil module.  Works with configuration data for account addresses/keys, etc.
"""


__TOOL = "zil_01.py"
__VERSION = "0.2.6-b35"
__DESC = "."

from pyzil.zilliqa import chain
from pyzil.account import Account
from pyzil.contract import Contract
from src.config.config import Config


debug_level = 2

#
def debug_print(level=3, *var_args):
    if level >= debug_level:
        print(*var_args)


#
class Zil_01(object):
    """Zilliqa interface class - support smart-contract deployment and
       functional interfacing."""
    net = None              # Which net - (chain.TestNet for testing)
    account = None          # Account Address
    contract = None         # Contract Object
    transaction = {         # (Initialised to default values below)
        'gas_limit' : 100000,
        'timeout' :   300,
        'sleep' :     10,
    }

    def __init__(self, account=None, account_address=None, net=None):
        """Zil_01 constructor function."""
        #  Setup and activate the required network ...
        if net == None:
            self.net = chain.TestNet
        else:
            self.net = net
        #chain.set_active_chain(chain.TestNet)
        chain.set_active_chain(self.net)

        #  Setup account ...
        if account:
            self.account = account
        else:
            if account_address:
                self.account = Account(address=account_address)
            else:
                #  Get default account details, from config ...
                #  [Add error trapping/check that json file exists]
                keystore_file = Config.keystore_file
                keystore_pwd = Config.keystore_passphrase
                self.account = Account.from_keystore(keystore_pwd,
                                                     keystore_file)
        debug_print(3, f"self.account:  {self.account}")


    def compile_and_deploy(self, filename, account=None, init_params=None):
        """Compile and deploy a smart contract, from scilla code in
        filename."""
        status = None
        debug_print(3,f"Compiling contract file: {filename}")
        contract = self.compile_contract(filename, account=account)
        #contract = self.compile_contract(filename)
        if contract:
            debug_print(3,f"Deploying contract ...")
            status = self.deploy_contract(init_params=init_params)
        else:
            debug_print(3,f"Warning: Contract not available")
        return (contract, status)


    def compile_contract(self, filename, account=None):
        """Compile smart contract, from scilla code in filename."""
        code = open(filename).read()
        self.contract = Contract.new_from_code(code)
        debug_print(3, f"Contract status:  {self.contract.status}")
        if account:
            self.account = account
        if self.contract:
            self.contract.account = self.account
        debug_print(3, f"Account:  {account}")
        return self.contract


    def deploy_contract(self, contract=None, init_params=None):
        """Deploy the smart contract, either from current contract (default)
        or from passed in contract object"""
        gas_limit = self.transaction['gas_limit']
        timeout = self.transaction['timeout']
        sleep = self.transaction['sleep']
        debug_print(3, f"Deploying contract:  {contract}")
        if not contract:
            txn_details = self.contract.deploy(init_params=init_params, 
                             gas_limit=gas_limit, timeout=timeout, sleep=sleep)
            receipt = self.contract.last_receipt
            status = self.contract.status
        else:
            txn_details = contract.deploy(init_params=init_params, 
                             gas_limit=gas_limit, timeout=timeout, sleep=sleep)
            receipt = self.contract.last_receipt
            status = self.contract.status
        if receipt is not None and receipt['success'] is True:
            #address = self.contract.address
            debug_print(3, f"Address:  {self.contract.address}")
        else:
            debug_print(3, f"Deploy failed.  Receipt: {receipt}")

        if status == Contract.Status.Deployed:
            debug_print(3, f"Status:  {status}")
        return status


    #  [** Add ability to select specific contract [e.g. by contract name??] **]
    def get_contract(self, offset=-1):
        """Get a contract address, using a supplied offset.  If no offset is 
        supplied the last available contract address will be used."""
        #  Set the contract to be the last deployed one ...
        owner_addr = self.account.address
        contracts = Contract.get_contracts(owner_addr)
        contract_addr = contracts[offset].address
        return contract_addr


    def load_contract(self, contract=None, address=None):
        """Load a particular contract and associate with the user's account."""
        #  [Make this smarter] ...
        if address is None:
            self.address = Config.default_contract_address
        else:
            self.address = address
        if contract is None:
            debug_print(3, f"Contract address:  {contract}")
            self.contract = Contract.load_from_address(self.address,
                                                       load_state=True)
            self.contract.account = self.account
        else:
            self.contract = contract
        return self.contract


    def get_balance(self):
        """..."""
        #  Set the contract to be the last deployed one ...
        balance = self.account.get_balance()
        return balance


if __name__ == '__main__':
    print("%s (%s-%s)" % (__TOOL, __VERSION, __DESC))
