#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# testgen_loc_player.py
# Zilliqa dapp Project - Machine Economy
# Copyright (c) 2019  Well Bred Software Limited and Rustiq Technology Limited
# This code is licensed under the MIT license (see LICENSE for terms).

"""
testgen_loc_player.py
Location test player - replays test data sequence from csv file and generates
out-of-bounds events to Zilliqa network.

Usage:
  testgen_loc_player.py [csv_data_filename]

Modules used: pyzil, zil_01
"""


#  Fix-up the path to the 'root' directory ...
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Modules ...
import time
import csv
import threading
import copy
from pyzil.contract import Contract
from pyzil.zilliqa.chain import active_chain

import src.zil_01 as zil_01


__TOOL = "testgen_loc_player.py"
__VERSION = "0.2.6-b35"
__DESC = "First release"

debugOn = True
debugOn = False


#  Default data file to load ...
filename = "data/location_test_data_output.csv"


def get_data(data_filename):
    """Process the input data."""
    data = []
    with open(data_filename, newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            if row != []:
                #print(row)
                data.append(row)
            else:
                pass     #  Empty row
    return data


#  Set up bounds object (LocationBounds) ...
class LocationBounds(object):
    is_oob = False
    oob_count = 0
    last_oob = 0.0
    oob_holdoff = 10.0  #  Minimum recovery time for new OOB Event


def setup_zil():
    """Do setup of zil_01 object and config"""
    #
    #  Get the zil object ...
    zil = zil_01.Zil_01(account=None)

    balance1 = zil.account.get_balance()
    print("Balance (initial):", balance1)

    #
    #  ... Set-up the contract ...
    contract = zil.get_contract()
    zil.load_contract(address=contract)

    return zil


bounds = None
zil = None
threads = []


def send_sc_event_t(asset_name,t,event_type,event_params):
    """Process the outbound event - send to SC transition receiveOobEvent"""
    if debugOn: print(f"send_sc_event_t({asset_name,t,event_type,event_params}) - Started  {time.ctime()}")

    #  Setup the zil object for this thread ...
    zil_t = setup_zil()

    #  Set params and call the contract receiveOobEvent transition ...
    gas_factor = 1
    my_gas_price = int(active_chain.api.GetMinimumGasPrice()) * gas_factor
    my_gas_limit = 10000
    if debugOn: print(f"send_sc_event():  my_gas_limit: {my_gas_limit}    "
          f"my_gas_price: {my_gas_price}")
    
    #  Set up params for the scilla contract ...
    params = [
        Contract.value_dict("event_type", "String", f"{event_type}"),
        Contract.value_dict("asset_name", "String", f"{asset_name}"),
    ]
    if debugOn: print(f"[receiveOobEvent call()]: params: {params}")
    
    #  Call the resetHello function ...
    if debugOn: print(f"zil_t.contract: {zil_t.contract}")
    zil_t.contract.call(method="receiveOobEvent",
                             gas_price=my_gas_price,
                             gas_limit=my_gas_limit,
                             params=params)
    if zil_t.contract.last_receipt:
        receipt = zil_t.contract.last_receipt
        if debugOn: print(f"receipt:  {receipt}")
        if receipt['success'] is True:
            print(f"send_sc_event_t() - Success.   {time.ctime()}")
        else:
            print(f" send_sc_event_t() Error: Transaction failed.  Errors: {receipt['errors']}")
    else:
        print(f"Error: No last_receipt in contract")
    if debugOn: print(f"send_sc_event_t() - Finished  {time.ctime()}")
    return


def send_sc_event(asset_name,t,event_type,event_params):
    """SC event - create thread and call handling routine"""
    if debugOn: print(f"send_sc_event({asset_name,t,event_type,event_params})")
    #  Add handling for OOB Event notification to SC ...
    thread = threading.Thread( \
        target=send_sc_event_t, args=(asset_name,t,event_type,event_params,))
    thread.start()
    if debugOn: print(f" ***  Starting thread: {thread.name}   ({time.ctime()})")
    return thread


maxThreads = 8


def process_next_location(t,point,polygon):
    #print(f"{t:.3f}, {point}")
    event_time = t
    thr = None
    #polygon = zil_01_location.check_in_bounds(point, bounds.bounds_data)
    found = not polygon is None
    if not found:
        print(f"Point {point} not in bounds (t: {t:.3f})")
        #   See if hold-off time has expired ...
        if not bounds.is_oob and \
           (bounds.last_oob + bounds.oob_holdoff) < event_time:
            bounds.is_oob = True
            bounds.oob_count += 1
            print(f"New OOB Event: {bounds.oob_count}   (t: {t:.3f})")
            #  Send event to SC ...
            asset_name = 'Asset_1'
            event_type,event_params = 'OOB_Event:New',[]
            if len(threads) < maxThreads:
                thr = send_sc_event(asset_name,t,event_type,event_params)
        bounds.last_oob = event_time
    else:
        print(f"Point {point} found in polygon: {polygon}")
        if bounds.is_oob and \
           (bounds.last_oob + bounds.oob_holdoff) < event_time:
            bounds.is_oob = False
            print(f"OOB Event: (Recovered) {bounds.oob_count}   (t: {t:.3f})")
            #  Send event to SC ...
            asset_name = 'Asset_1'
            event_type,event_params = 'OOB_Event:Recovered',[]
            thr = send_sc_event(asset_name,t,event_type,event_params)
    return thr


def main(argv=None):
    """Example app for exercising Zil_01 class."""
    global bounds
    global threads

    #  Get contract filename from cli params, if present ...
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    #  Get the bounds object ...
    bounds = LocationBounds()

    #  Load the data table ...
    file_data = get_data(filename)
    if len(file_data) > 1:
        output_data = file_data[1:]

    iteration_period = 1
    polygon = None
    now = time.time()
    start_time = now
    next_time = start_time
    print(f"output_data[0]: {output_data[0]}")
    point = (float(output_data[0][1]), float(output_data[0][2]), float(output_data[0][3]))
    polygon = int(output_data[0][4]) if output_data[0][4] == "None" else None
    in_bounds = not polygon is None
    #  Process the initial point ...
    print(f"start_time, point, polygon: {start_time, point, polygon}")
    res = process_next_location(start_time, point, polygon)
    
    print()
    print(f"Initial point (t0) is: {point}) ...")
    print()
    print(f"Generated sequence data (period: {iteration_period}) ...")
    try:
        for d in output_data[1:]:
            #  Process the point ...
            t = float(d[0])
            point = (float(d[1]), float(d[2]), float(d[3]))
            polygon = int(d[4]) if d[4] and not d[4] == "None" else None
            in_bounds = not polygon is None
            next_time = start_time + t 
            now = time.time()
            time.sleep(max(0, next_time - now))
            #  [** Add action processing here **]
            now = time.time()
            #  Process the point ...
            res = process_next_location(now, point, polygon)
            #  Capture the data point (and in-bounds status) ..
            if res:  threads += [res]
    except KeyboardInterrupt:
        print(f"\n** User interrupt **")
    print(f"Location sequence completed (at {time.ctime()}) ")
    print(f"\nWaiting for threads ({len(threads)}):   {time.ctime()} ...")
    #
    for thr in threads:
        if debugOn: print(f" ***  Joining thread:  {thr.name}")
        thr.join()


if __name__ == '__main__':
    print("%s (%s-%s)" % (__TOOL, __VERSION, __DESC))

    print(f"Started:   {time.ctime()}")
    main()
    print()
    print(f"Finished:  {time.ctime()}")
