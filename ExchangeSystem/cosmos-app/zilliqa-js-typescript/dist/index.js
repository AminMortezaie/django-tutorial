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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const body_parser_1 = __importDefault(require("body-parser"));
const experiment_1 = __importDefault(require("./experiment"));
const app = (0, express_1.default)();
app.use(body_parser_1.default.json());
app.get('/api/', (req, res) => {
    res.send("Hello this is my zilliqa-js-typescript app.");
});
app.post('/api/broadcast-transaction', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    console.log(req.body);
    const transaction = {
        to_address: req.body.to_address,
        private_key: req.body.private_key,
        amount: req.body.amount
    };
    const message = yield (0, experiment_1.default)(transaction);
    res.status(201).json({
        message
    });
}));
const port = process.env.PORT || 3001;
app.listen(port, () => console.log(`App is listening on PORT ${port}`));
