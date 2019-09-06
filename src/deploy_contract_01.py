#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#******************************************************************************
#* Filename:            deploy_contract_01.py
#* Last Updated:        2019-09-05
#* Status:              Prototype
#* Description:         Basic script to assist in contract deployment
#* Project:             Zilliqa dApp Project
#******************************************************************************
#*     Copyright (c) 2019 Well Bred Software Limited (on behalf of DX3 Core)
#*                           All rights reserved
#******************************************************************************

#  cd 

__TOOL = "deploy_contract_01.py"
__VERSION = "0.2.0-b20"
__DESC = "Initial github release"

import sys
import time
import zil_01


if __name__ == '__main__':
    print("%s (%s-%s)" % (__TOOL, __VERSION, __DESC))

filename = "src/me_ex1_oob_loc.scilla"
filename = "src/me_tmp_01.scilla"

if len(sys.argv) > 1:
    filename = sys.argv[1]

start = time.time()
print(f"Starting at: {time.ctime(start)}")

zil = zil_01.Zil_01(account=None)

zil.debug_level = 3

#  Adjust gas_limit value ...
zil.transaction['gas_limit'] = 20000

print("Deploying contract in:", filename)

balance1 = zil.account.get_balance()
print("Balance (before):", balance1)

start_deploy = time.time()
print(f"Starting (compile and) deployment at: {time.ctime(start_deploy)}")

contract, status = zil.compile_and_deploy(filename)
end_deploy = time.time()
print(f"Ending deployment at: {time.ctime(end_deploy)}  Duration: {end_deploy - start_deploy}s")

print(f"Outcome: Status: {status}   Contract: {contract}")

balance2 = zil.account.get_balance()
print("Balance (after):", balance2)

print("Zil used (deployment):", balance1 - balance2)

end = time.time()

print(f"Ending at: {time.ctime(end)}  Duration: {end - start}s")

#if __name__ == '__main__':
#    print("%s (%s-%s)" % (__TOOL, __VERSION, __DESC))


"""
#  Individual compile / deploy methods ...

contract = zil.compile_contract(filename)
print(f"Contract status: {zil.contract.status}")

status = zil.deploy_contract()
print(f"Outcome: Status: {status}")

"""
