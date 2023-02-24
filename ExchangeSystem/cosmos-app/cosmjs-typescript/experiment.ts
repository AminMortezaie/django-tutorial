import { IndexedTx, SigningStargateClient, StargateClient, DeliverTxResponse } from "@cosmjs/stargate"
import { Tx } from "cosmjs-types/cosmos/tx/v1beta1/tx"
import { MsgSend } from "cosmjs-types/cosmos/bank/v1beta1/tx"
import {Transaction} from "./index.js"
import { DirectSecp256k1HdWallet, OfflineDirectSigner } from "@cosmjs/proto-signing"


const rpc = "rpc.sentry-01.theta-testnet.polypore.xyz:26657"


const getFromAddressSignerFromMnemonic = async (seed:string): Promise<OfflineDirectSigner> => {
    return DirectSecp256k1HdWallet.fromMnemonic((seed).toString(), {
        prefix: "cosmos",
    })
}




const runAll = async(transaction: Transaction): Promise<DeliverTxResponse> => {
    const fromAddress = transaction.from_address
    const toAddress = transaction.to_address
    const seed = transaction.seed
    const amount = transaction.amount

    const client = await StargateClient.connect(rpc)
    console.log("With client, chain id:", await client.getChainId(), ", height:", await client.getHeight())

    
    const faucetTx: IndexedTx = (await client.getTx(
        "A1D7733898BFC29DB13672DF03C065EA5F2DF3ABC3C06E427FB114CB05E7D901",
    ))!
    const decodedTx: Tx = Tx.decode(faucetTx.tx)
    const sendMessage: MsgSend = MsgSend.decode(decodedTx.body!.messages[0].value)
    console.log("Sent message:", sendMessage)

    
    const fromAddressSigner: OfflineDirectSigner = await getFromAddressSignerFromMnemonic(seed)
    // const from_address = (await aliceSigner.getAccounts())[0].address
    // const faucet = "cosmos1zamzgclq5ck48q6qcxrlvqd5fsmne295yfw9dp"
    console.log("Sender's address from signer", fromAddress)
    const signingClient = await SigningStargateClient.connectWithSigner(rpc, fromAddressSigner)
    console.log(
        "With signing client, chain id:",
        await signingClient.getChainId(),
        ", height:",
        await signingClient.getHeight()
    )
    
    
    console.log("Gas fee:", decodedTx.authInfo!.fee!.amount)
    console.log("Gas limit:", decodedTx.authInfo!.fee!.gasLimit.toString(10))


    // Check the balance of Alice and the Faucet
    console.log("Alice balance before:", await client.getAllBalances(fromAddress))
    console.log("Faucet balance before:", await client.getAllBalances(toAddress))
    // Execute the sendTokens Tx and store the result
    const result = await signingClient.sendTokens(
        fromAddress,
        toAddress,
        [{ denom: "uatom", amount: amount }],
        {
            amount: [{ denom: "uatom", amount: "500" }],
            gas: "200000",
        },
    )
    // Output the result of the Tx
    return result   
}

export default runAll;