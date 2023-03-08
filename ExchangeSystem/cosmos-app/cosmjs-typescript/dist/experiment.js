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
const stargate_1 = require("@cosmjs/stargate");
const proto_signing_1 = require("@cosmjs/proto-signing");
// const rpc = "https://cosmos-mainnet-rpc.allthatnode.com:26657" //mainnet
const rpc = "rpc.sentry-01.theta-testnet.polypore.xyz:26657"; //testnet
const getFromAddressSignerFromMnemonic = (seed) => __awaiter(void 0, void 0, void 0, function* () {
    return proto_signing_1.DirectSecp256k1HdWallet.fromMnemonic((seed).toString(), {
        prefix: "cosmos",
    });
});
const runAll = (transaction) => __awaiter(void 0, void 0, void 0, function* () {
    const fromAddress = transaction.from_address;
    const toAddress = transaction.to_address;
    const seed = transaction.seed;
    const amount = Math.floor(parseFloat(transaction.amount) * 10000000);
    console.log("this is amount", amount);
    const memo = transaction.memo;
    console.log("this is memo", memo);
    const client = yield stargate_1.StargateClient.connect(rpc);
    console.log("With client, chain id:", yield client.getChainId(), ", height:", yield client.getHeight());
    // const faucetTx: IndexedTx = (await client.getTx(
    //     "A1D7733898BFC29DB13672DF03C065EA5F2DF3ABC3C06E427FB114CB05E7D901",
    // ))!
    // const decodedTx: Tx = Tx.decode(faucetTx.tx)
    // const sendMessage: MsgSend = MsgSend.decode(decodedTx.body!.messages[0].value)
    // console.log("Sent message:", sendMessage)
    const fromAddressSigner = yield getFromAddressSignerFromMnemonic(seed);
    // const from_address = (await aliceSigner.getAccounts())[0].address
    // const faucet = "cosmos1zamzgclq5ck48q6qcxrlvqd5fsmne295yfw9dp"
    console.log("Sender's address from signer", fromAddress);
    const signingClient = yield stargate_1.SigningStargateClient.connectWithSigner(rpc, fromAddressSigner);
    console.log("With signing client, chain id:", yield signingClient.getChainId(), ", height:", yield signingClient.getHeight());
    // console.log("Gas fee:", decodedTx.authInfo!.fee!.amount)
    // console.log("Gas limit:", decodedTx.authInfo!.fee!.gasLimit.toString(10))
    // Check the balance of Alice and the Faucet
    console.log("Alice balance before:", yield client.getAllBalances(fromAddress));
    console.log("Faucet balance before:", yield client.getAllBalances(toAddress));
    // Execute the sendTokens Tx and store the result
    const result = yield signingClient.sendTokens(fromAddress, toAddress, [{ denom: "uatom", amount: amount.toString() }], {
        amount: [{ denom: "uatom", amount: "500" }],
        gas: "200000",
    }, memo);
    // Output the result of the Tx
    return result;
});
exports.default = runAll;
