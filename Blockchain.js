const Block = require('./Block');
const { generateHash } = require('./HashUtil');

class Blockchain {
  constructor() {
    this.blocks = [];
    this.nodes = [];
    this.currentTransactions = [];
    this.createGenesisBlock();
    this.hashingAlgorithm = 'SHA256';
  }
  
  setHashingAlgorithm(algorithm) {
    this.hashingAlgorithm = algorithm;
  }
      addNode(node) {
      this.nodes.push(node);
    }
  
    createGenesisBlock() {
    const genesisBlock = new Block([], null);
    genesisBlock.computeHash();
    this.blocks.push(genesisBlock);
  }

  addTransaction(transaction) {
    this.currentTransactions.push(transaction);
    if (this.currentTransactions.length >= 11) { // Modificar el límite a 11
      this.createBlock();
    }
  }

    createBlock() {
    const block = new Block(this.currentTransactions, this.getLastBlockHash());
    block.computeHash();
    this.blocks.push(block);
    this.currentTransactions = [];
    this.broadcastBlock(block);
  }

  getLastBlockHash() {
    if (this.blocks.length === 0) {
      return null;
    }
    return this.blocks[this.blocks.length - 1].hash;
  }

  broadcastBlock(block) {
    // Implementación de la lógica para transmitir el bloque a otros nodos o componentes
    console.log('Broadcasting Block:', block);
  }
   }
module.exports = Blockchain;
