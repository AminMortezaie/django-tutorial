"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const { Transaction } = require('@zilliqa-js/account');
const { BN, Long, bytes, units } = require('@zilliqa-js/util');
const { Zilliqa } = require('@zilliqa-js/zilliqa');
const CP = require('@zilliqa-js/crypto');
const CHAIN_ID = 1;
const MSG_VERSION = 1;
const VERSION = bytes.pack(CHAIN_ID, MSG_VERSION);
const zilliqa = new Zilliqa('https://api.zilliqa.com');
const runAll = (transaction) => __awaiter(void 0, void 0, void 0, function* () {
    const privateKey = transaction.private_key;
    const toAddress = transaction.to_address;
    console.log(privateKey, toAddress);
    const amount = new BN(units.toQa(parseFloat(transaction.amount), units.Units.Zil));
    zilliqa.wallet.addByPrivateKey(privateKey);
    const address = CP.getAddressFromPrivateKey(privateKey);
    console.log("Your account address is:");
    console.log(`0x${address}`);
    try {
        // Get Balance
        const balance = yield zilliqa.blockchain.getBalance(address);
        // Get Minimum Gas Price from blockchain
        const minGasPrice = yield zilliqa.blockchain.getMinimumGasPrice();
        console.log(`Your account balance is:`);
        console.log(balance.result);
        console.log(`Current Minimum Gas Price: ${minGasPrice.result}`);
        const myGasPrice = units.toQa('2000', units.Units.Li); // Gas Price that will be used by all transactions
        console.log(`My Gas Price ${myGasPrice.toString()}`);
        console.log('Sufficient Gas Price?');
        console.log(myGasPrice.gte(new BN(minGasPrice.result))); // Checks if your gas price is less than the minimum gas price
        // Send a transaction to the network
        const tx = yield zilliqa.blockchain.createTransaction(zilliqa.transactions.new({
            version: VERSION,
            toAddr: toAddress,
            amount: amount,
            gasPrice: myGasPrice,
            gasLimit: Long.fromNumber(50)
        }));
        console.log(`The transaction status is:`);
        console.log(tx.receipt);
        const result = tx.id;
        return { "tx": result };
    }
    catch (err) {
        console.log(err);
        return { err: err.message };
    }
});
exports.default = runAll;
