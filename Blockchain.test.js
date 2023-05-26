const Blockchain = require('./Blockchain');
const Transaction = require('./Transaction');
const { v4: uuidv4 } = require('uuid');
const { generateHash } = require('./HashUtil');
const crypto = require('crypto');
const Block = require('./Block');
const Token = require('./Token');

describe('Blockchain', () => {
  let blockchain;

  beforeEach(() => {
    blockchain = new Blockchain();
  });

  test('crear nuevos nodos', () => {
    const node = 'http://localhost:3001';
    blockchain.addNode(node);
    expect(blockchain.nodes).toContain(node);
  });

  test('agregar transacciones y validar integridad', () => {
    const transaction = new Transaction('Tx-123', 'A-456');
    transaction.computeHash();

    blockchain.addTransaction(transaction);
    expect(blockchain.currentTransactions).toContain(transaction);

    // Validar la integridad de la transacción
    const isTransactionValid = transaction.validateIntegrity();
    expect(isTransactionValid).toBe(true);
  });

  test('establecer y alterar el mecanismo de hashing', () => {
    const newHashingAlgorithm = 'MD5';

    // Establecer el algoritmo de hashing
    blockchain.setHashingAlgorithm(newHashingAlgorithm);
    expect(blockchain.hashingAlgorithm).toBe(newHashingAlgorithm);

    // Alterar el mecanismo de hashing nuevamente
    const anotherHashingAlgorithm = 'SHA512';
    blockchain.setHashingAlgorithm(anotherHashingAlgorithm);
    expect(blockchain.hashingAlgorithm).toBe(anotherHashingAlgorithm);
  });

  test('cerrar bloques al exceder el límite de transacciones', () => {
    // Agregar 11 transacciones para exceder el límite de bloque
    for (let i = 0; i < 11; i++) {
      const transaction = new Transaction(`Tx-${i}`, `A-${i}`);
      blockchain.addTransaction(transaction);
    }

    // Verificar que se haya creado un nuevo bloque y se hayan eliminado las transacciones pendientes
    expect(blockchain.blocks.length).toBe(2);
    expect(blockchain.currentTransactions.length).toBe(0);
  });

  test('calcular el último hash de bloque', () => {
    // Crear algunos bloques
    const block1 = new Block([], null);
    const block2 = new Block([], block1.hash);
    const block3 = new Block([], block2.hash);

    // Agregar los bloques a la cadena
    blockchain.blocks.push(block1);
    blockchain.blocks.push(block2);
    blockchain.blocks.push(block3);

    // Obtener el último hash de bloque
    const lastBlockHash = blockchain.getLastBlockHash();

    // Verificar que sea el hash correcto
    expect(lastBlockHash).toBe(block3.hash);
  });

  test('broadcast de un bloque', () => {
    // Crear un bloque para transmitir
    const block = new Block([], null);
    block.computeHash();

    // Capturar la salida del console.log
    console.log = jest.fn();

    // Llamar a la función de broadcastBlock
    blockchain.broadcastBlock(block);

    // Verificar que se haya llamado al console.log con el bloque correcto
    expect(console.log).toHaveBeenCalledWith('Broadcasting Block:', block);
  });

  test('calcular el hash de una transacción', () => {
    const tokenValue = 'TKN-123';
    const outValue = 'A-456';
    const transaction = new Transaction(tokenValue, outValue);

    // Calcular el hash de la transacción
    transaction.computeHash();

    // Verificar que el hash se haya calculado correctamente
    expect(transaction.hash).toBeDefined();
    expect(typeof transaction.hash).toBe('string');
    expect(transaction.hash.length).toBe(64);

    // Verificar que el hash sea consistente con los datos de la transacción
    const data = JSON.stringify({
      id: transaction.id,
      token: tokenValue,
      out: outValue,
      inTransactionId: null,
    });
    const expectedHash = crypto.createHash('sha256').update(data).digest('hex');
    expect(transaction.hash).toBe(expectedHash);
  });

  test('transmitir un bloque', () => {
    // Crea un bloque para transmitir
    const block = new Block([], null);
    block.computeHash();

    // Captura la salida de console.log
    console.log = jest.fn();

    // Llama a la función de broadcastBlock
    blockchain.broadcastBlock(block);

    // Verifica que se haya llamado a console.log con el bloque correcto
    expect(console.log).toHaveBeenCalledWith('Broadcasting Block:', block);
  });

  describe('Token', () => {
  test('convertir a cadena', () => {
    // Genera un identificador UUID único
    const uuid = uuidv4();

    // Crea una instancia de Token
    const token = new Token();

    // Llama al método toString() para obtener la representación de cadena
    const tokenString = token.toString();

    // Verifica que la cadena generada tenga el formato correcto
    const expectedString = `TKN ${token.id.split(' ')[1]}`;
    expect(tokenString).toBe(expectedString);
  });
});



  describe('HashUtil', () => {
    test('generar hash de un bloque a partir de sus atributos', () => {
      const timestamp = 1629785438000; // Timestamp en milisegundos
      const transactions = ['tx1', 'tx2', 'tx3']; // Lista de transacciones
      const previousHash = 'abc123'; // Hash del bloque anterior
      const block = { timestamp, transactions, previousHash };
  
      // Corregir la prueba asegurándose de que todas las propiedades del bloque estén definidas
      const timestampString = block.timestamp.toString();
      const transactionsString = JSON.stringify(block.transactions);
      const previousHashString = block.previousHash.toString();
      const data = timestampString + transactionsString + previousHashString;
      const hash = generateHash(data);
  
      expect(hash).toBeDefined();
      expect(typeof hash).toBe('string');
      expect(hash.length).toBe(64);
    });
    test('alternar algoritmo de hashing entre SHA256 y MD5', () => {
      const data = 'example data';
    
      // Generar hash utilizando el algoritmo SHA256
      blockchain.setHashingAlgorithm('SHA256');
      const hash1 = generateHash(data);
    
      // Alternar algoritmo a MD5
      blockchain.setHashingAlgorithm('MD5');
      const md5Hash1 = generateHash(data);
    
      // Alternar algoritmo nuevamente a SHA256
      blockchain.setHashingAlgorithm('SHA256');
      const hash2 = generateHash(data);
    
      expect(hash1).toBe(hash2);
      });
    
    test('generar hash de un bloque sin transacciones', () => {
      const timestamp = 1629785438000;
      const transactions = [];
      const previousHash = 'abc123';
      const block = { timestamp, transactions, previousHash };
  
      // Corregir la prueba asegurándose de que todas las propiedades del bloque estén definidas
      const timestampString = block.timestamp.toString();
      const transactionsString = JSON.stringify(block.transactions);
      const previousHashString = block.previousHash.toString();
      const data = timestampString + transactionsString + previousHashString;
      const hash = generateHash(data);
  
      expect(hash).toBeDefined();
      expect(typeof hash).toBe('string');
      expect(hash.length).toBe(64);
    });
  });
  });
