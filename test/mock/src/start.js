/*
 * This file is part of Machine Economy Zilliqa Dapp Project.
 *
 * Copyright (c) 2019 Rustiq Technology Ltd & Well Bred Software Ltd
 * MIT License
 */

var app = require('../kaya/src/app');
var assert = require('chai').assert;
var expect = require('chai')
    .use(require('chai-as-promised'))
    .expect;
var fs = require('fs');
var path = require('path');

const SERVER_PORT = 4200;
const RUNTIME_DIR = path.join(__dirname, '../runtime-data');

function main() {
    console.log(' +++++ Starting the Kaya server +++++ ');
    // The ExpressJS object of the Kaya server.
    var server = app.expressjs.listen(SERVER_PORT, (err) => {
        if (err) {
            process.exit(1);
        }
    });
    // The accounts created by Kaya that can be used throughout the test sequence after initialisation.
    var accounts = app.wallet.getAccounts();
    expect(accounts).to.be.an('object');
    expect(accounts).to.not.be.empty;
    var accounts_s = JSON.stringify(accounts, null, 4);
    if (!fs.existsSync(RUNTIME_DIR)) {
        fs.mkdirSync(RUNTIME_DIR);
    }
    var filePath = path.join(RUNTIME_DIR, 'accounts.json');
    fs.writeFileSync(filePath, accounts_s);
    console.log(` ***** Initial account data saved to ${filePath} *****`);
}

main();
