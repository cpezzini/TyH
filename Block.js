const crypto = require('crypto');
const { generateHash } = require('./HashUtil');

class Block {
  constructor(transactions, previousHash) {
    this.timestamp = Date.now();
    this.transactions = transactions;
    this.previousHash = previousHash;
    this.hash = null;
  }

  computeHash() {
    const data = JSON.stringify({
      timestamp: this.timestamp,
      transactions: this.transactions,
      previousHash: this.previousHash,
    });
    this.hash = crypto.createHash('sha256').update(data).digest('hex');
  }
}

module.exports = Block;
