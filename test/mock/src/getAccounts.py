# This file is part of Machine Economy Zilliqa Dapp Project.
#
# Copyright (c) 2019 Rustiq Technology Ltd & Well Bred Software Ltd
# MIT License

import json

# A public map of account addresses to their private keys.
accountPrivateKeys = {}

with open('../runtime-data/accounts.json') as accountsFile:
    accounts = json.load(accountsFile)
    for a in accounts:
        accountPrivateKeys[a] = accounts[a]['privateKey']
