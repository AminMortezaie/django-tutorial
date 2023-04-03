import express from 'express';
import bodyParser from 'body-parser';
import runAll  from './experiment';



const app = express()
app.use(bodyParser.json());

export interface Transaction{
    private_key:string,
    to_address: string,
    amount:string
}


app.get('/api/', (req, res) => {
    res.send("Hello this is my zilliqa-js-typescript app.");
});

app.post('/api/broadcast-transaction', async(req, res)=>{
    console.log(req.body)
    
    const transaction: Transaction = {
      to_address: req.body.to_address, 
      private_key: req.body.private_key,
      amount: req.body.amount
    };
    const message = await runAll(transaction)
  
    res.status(201).json({
        message
      });
});



const port = process.env.PORT || 8080;

app.listen(port, ()=>console.log(`App is listening on PORT ${port}`));



