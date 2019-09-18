/*
 * This file is part of Machine Economy Zilliqa Dapp Project.
 *
 * Copyright (c) 2019 Rustiq Technology Ltd & Well Bred Software Ltd
 * MIT License
 */

var app = require('../kaya/src/app');
const assert = require('chai').assert;
const expect = require('chai')
      .use(require('chai-as-promised'))
      .expect;

const SERVER_PORT = 4200;

var server;
// The accounts created by Kaya that can be used throughout the test sequence after initialisation.
var accounts;

describe('Mock tests run on the Kaya server', () => {
    before(async () => {
        // Start the Kaya server.
        server = app.expressjs.listen(SERVER_PORT, (err) => {
            if (err) {
                process.exit(1);
            }
        });
    });

    it('Get the initial account addresses and their private keys', async () => {
        var accounts = app.wallet.getAccounts();
        console.log(' ***** Wallet accounts: *****\n', JSON.stringify(accounts, null, 4));
        expect(accounts).to.be.an('object');
        expect(accounts).to.not.be.empty;
    });

    it('Server terminates', async () => {
        server.close();
    });

    // FIXME: This doesn't allow mocha to print statistics.
    after(async () => {
        console.log(' ***** Forcing Kaya to terminate... *****'),
        process.exit(0);
    });
});
