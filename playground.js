const Token = require('./Token');
const Transaction = require('./Transaction');
const Blockchain = require('./Blockchain');
const { generateHash } = require('./HashUtil');

// Crear una instancia de la blockchain
const blockchain = new Blockchain();

// Crear un token
const token = new Token('abcd-1234');
// Crear una transacción coinbase
const coinbaseTransaction = new Transaction(token, 'A-1234');
coinbaseTransaction.computeHash();

// Agregar la transacción coinbase a la blockchain
blockchain.addTransaction(coinbaseTransaction);

// Crear transacciones normales
const transaction1 = new Transaction(token, 'A-5678', coinbaseTransaction.id);
transaction1.computeHash();

const transaction2 = new Transaction(token, 'A-9012', transaction1.id);
transaction2.computeHash();

// Agregar las transacciones normales a la blockchain
blockchain.addTransaction(transaction1);
blockchain.addTransaction(transaction2);
