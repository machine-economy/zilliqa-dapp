#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#******************************************************************************
#* Filename:            deploy_contract_01.py
#* Last Updated:        2019-09-30
#* Status:              Prototype
#* Description:         Basic script to assist in contract deployment
#* Project:             Zilliqa dApp Project
#******************************************************************************
#*     Copyright (c) 2019 Well Bred Software Limited (on behalf of DX3 Core)
#*                           All rights reserved
#******************************************************************************

#  cd 

__TOOL = "deploy_contract_01.py"
__VERSION = "0.2.4-b27"
__DESC = "Refactored into main(); Added payee_account setup in init params"

#  Fix-up the path to the 'root' directory ...
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import src.zil_01 as zil_01
from pyzil.contract import Contract
from pyzil.account import Account


filename = "src/me_tmp_01.scilla"
filename = "src/contracts/me_ex1_oob_loc.scilla"

def main(argv):
    global filename

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    start = time.time()
    print(f"Starting at: {time.ctime(start)}")
    
    zil = zil_01.Zil_01(account=None)
    
    print("Account address:", zil.account.address)
    
    zil.debug_level = 3
    
    #  Adjust gas_limit value ...
    zil.transaction['gas_limit'] = 2000000000
    zil.transaction['gas_limit'] = 20000
    
    print("Deploying contract from file:", filename)
    
    balance1 = zil.account.get_balance()
    print("Balance (before):", balance1)
    
    #  Setup the payee account ...
    '''
    keystore_file = Config.keystore_file
    keystore_pwd = Config.keystore_passphrase
    account = Account.from_keystore(keystore_pwd, keystore_file)
    '''
    payee_account = Account(
                           address="zil1fftsz0t5lvdlhlhj4cal9xzva9cvulmz5tv7sx")

    start_deploy = time.time()
    print(f"Starting (compile and) deployment at: {time.ctime(start_deploy)}")
    
    #  Define the params for the contract ...
    init_params = [
        #Contract.value_dict("payee", "ByStr20", zil.account.address0x),
        Contract.value_dict("payee", "ByStr20", payee_account.address0x),
        Contract.value_dict("penaltyThreshold", "Uint32", "4"),
        Contract.value_dict("penaltyAmount", "Uint128", "10"),
    ]
    
    contract, status = zil.compile_and_deploy(filename, init_params=init_params)
    end_deploy = time.time()
    print(f"Ending deployment at: {time.ctime(end_deploy)}  Duration: {end_deploy - start_deploy}s")
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

if __name__ == '__main__':
    print("%s (%s-%s)" % (__TOOL, __VERSION, __DESC))
    main(sys.argv)
