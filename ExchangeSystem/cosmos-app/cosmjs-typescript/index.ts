import express from 'express';
import bodyParser from 'body-parser';
import runAll  from './experiment';



const app = express()
app.use(bodyParser.json());

interface Post {
    title: string;
    content: string;
  }

  const posts: Post[] = [
    {
      title: 'First post',
      content: 'This is the first post'
    },
    {
      title: 'Second post',
      content: 'This is the second post'
    }
  ];

export interface Transaction{
    from_address: string,
    to_address: string, 
    seed:string, 
    amount:string,
    memo:string
}


app.get('/api/', (req, res) => {
    res.send("Hello this is my typescript app.");
});

app.post('/api/broadcast-transaction', async(req, res)=>{
    
    const transaction: Transaction = {
      from_address: req.body.from_address,
      to_address: req.body.to_address, 
      seed: req.body.seed, 
      amount: req.body.amount,
      memo: req.body.memo
    };
    const message = await runAll(transaction)
  
    res.status(201).json({
        message
      });
});


// app.get('/api/run-all', async(req, res)=>{
//   const transaction: Transaction = {
//     from_address: req.body.from_address,
//     to_address: req.body.to_address,
//     seed: req.body.seed,
//     amount: req.body.amount
//   };
//
//     const response = await runAll(transaction)
//     const postsJSON = JSON.stringify(response);
//     res.setHeader('Content-Type', 'application/json');
//     res.send(response)
// });



const port = process.env.PORT || 3000;

app.listen(port, ()=>console.log(`App is listening on PORT ${port}`));



