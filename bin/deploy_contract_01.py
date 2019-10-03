#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# deploy_contract_01.py
# Zilliqa dApp Project - Machine Economy
# Copyright (c) 2019  Well Bred Software Limited (on behalf of DX3 Core)
# MIT License [TBC]

# Contract deployment tool - deploys contract to Zilliqa network.
# 
# Uses: zil_01 module, pyzil module


#  Fix-up the path to the 'root' directory ...
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
from pyzil.contract import Contract
from pyzil.account import Account

import src.zil_01 as zil_01
from src.config.config import Config


__TOOL = "deploy_contract_01.py"
__VERSION = "0.2.5-b30"
__DESC = "Refactored into main(); Added payee_account setup in init params"


#  Default contract to deploy.
filename = "src/contracts/me_ex1_oob_loc.scilla"


def main(argv):
    """Main script function"""
    global filename

    #  Get contract filename from cli params, if present ...
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    start = time.time()
    print(f"Starting at: {time.ctime(start)}")
    
    #  Setup the zil object (with default account, from config) ...
    zil = zil_01.Zil_01(account=None)
    
    print("Account address:", zil.account.address)
    
    zil.debug_level = 3
    
    #  Adjust gas_limit value ...
    zil.transaction['gas_limit'] = 20000
    
    print("Deploying contract from file:", filename)
    
    balance1 = zil.account.get_balance()
    print("Balance (before):", balance1)
    
    #  Setup the payee account ...
    if 1:
        #  Get account from config data - account address
        payee_address = Config.payee_account_address
        payee_account = Account(address=payee_address)
    else:
        #  Get account from config data - keystore file
        payee_keystore_file = Config.payee_keystore_file
        payee_keystore_pwd = Config.payee_keystore_passphrase
        payee_account = Account.from_keystore(payee_keystore_pwd, 
            payee_keystore_file)

    start_deploy = time.time()
    print(f"Starting (compile and) deployment at: {time.ctime(start_deploy)}")
    
    #  Define the params for the contract ...
    penaltyThreshold = str(4)
    penaltyAmount = str(10)
    init_params = [
        Contract.value_dict("payee", "ByStr20", payee_account.address0x),
        Contract.value_dict("penaltyThreshold", "Uint32", penaltyThreshold),
        Contract.value_dict("penaltyAmount", "Uint128", penaltyAmount),
    ]
    
    contract, status = zil.compile_and_deploy(filename, init_params=init_params)
    end_deploy = time.time()
    print(f"Ending deployment at: {time.ctime(end_deploy)}")
    print(f"Duration: {end_deploy - start_deploy}s")
    print(f"contract.address: {contract.address}")
    
    print(f"Outcome: Status: {status}   Contract: {contract}")
    
    receipt = zil.contract.last_receipt
    
    if status.value != "Deployed":
        print(f"Deploy failed '{status}' - receipt:  {receipt}")
    
    balance2 = zil.account.get_balance()
    print("Balance (after):", balance2)
    
    print("Zil used (deployment):", balance1 - balance2)
    
    end = time.time()
    
    print(f"Ending at: {time.ctime(end)}  Duration: {end - start}s")


#  
if __name__ == '__main__':
    print("%s (%s-%s)" % (__TOOL, __VERSION, __DESC))
    main(sys.argv)
