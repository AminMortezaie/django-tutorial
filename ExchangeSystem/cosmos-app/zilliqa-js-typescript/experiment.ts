const { Transaction } = require('@zilliqa-js/account');
const { BN, Long, bytes, units } = require('@zilliqa-js/util');
const { Zilliqa } = require('@zilliqa-js/zilliqa');
import {Transaction} from "./index.js"
const CP = require ('@zilliqa-js/crypto');

const CHAIN_ID = 333;
const MSG_VERSION = 1;
const VERSION = bytes.pack(CHAIN_ID, MSG_VERSION);

const zilliqa = new Zilliqa('https://dev-api.zilliqa.com');






const runAll = async(transaction: Transaction): Promise<any> => {
    const privateKey = transaction.private_key
    const toAddress = transaction.to_address
    console.log(privateKey, toAddress)
    const amount = new BN(units.toQa(parseFloat(transaction.amount), units.Units.Zil))

    zilliqa.wallet.addByPrivateKey(privateKey);

    const address = CP.getAddressFromPrivateKey(privateKey);
    console.log("Your account address is:");
    console.log(`0x${address}`);

    try {
        // Get Balance
        const balance = await zilliqa.blockchain.getBalance(address);

        // Get Minimum Gas Price from blockchain
        const minGasPrice = await zilliqa.blockchain.getMinimumGasPrice();
        console.log(`Your account balance is:`);
        console.log(balance.result)
        console.log(`Current Minimum Gas Price: ${minGasPrice.result}`);

        const myGasPrice = units.toQa('2000', units.Units.Li); // Gas Price that will be used by all transactions
        console.log(`My Gas Price ${myGasPrice.toString()}`)
        console.log('Sufficient Gas Price?');
        console.log(myGasPrice.gte(new BN(minGasPrice.result))); // Checks if your gas price is less than the minimum gas price

        // Send a transaction to the network
        const tx = await zilliqa.blockchain.createTransaction(
          zilliqa.transactions.new({
            version: VERSION,
            toAddr: toAddress,
            amount: amount , // Sending an amount in Zil (1) and converting the amount to Qa
            gasPrice: myGasPrice, // Minimum gasPrice veries. Check the `GetMinimumGasPrice` on the blockchain
            gasLimit: Long.fromNumber(50)
          })
        );
        console.log(`The transaction status is:`);
        console.log(tx.receipt);
        const result = tx.id
        return {"tx": result}
      }catch (err) {
        console.log(err);
        return { err: (err as Error).message };
     }

    
}

export default runAll;