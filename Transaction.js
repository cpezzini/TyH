const { v4: uuidv4 } = require('uuid');
const { generateHash } = require('./HashUtil');
const crypto = require('crypto');
const Token = require('./Token');

class Transaction {
  constructor(token, out, inTransactionId = null) {
    this.id = `Tx-${uuidv4()}`;
    this.token = token;
    this.out = out;
    this.inTransactionId = inTransactionId;
    this.hash = null;
  }

  computeHash() {
    const data = JSON.stringify({
      id: this.id,
      token: this.token.toString(),
      out: this.out,
      inTransactionId: this.inTransactionId,
    });
    this.hash = crypto.createHash('sha256').update(data).digest('hex');
  }
  validateIntegrity() {
    const { id, token, out, inTransactionId, hash } = this;
    const data = JSON.stringify({
      id,
      token: token.toString(),
      out,
      inTransactionId,
    });
    const computedHash = crypto.createHash('sha256').update(data).digest('hex');
    return computedHash === hash;
  }
}

module.exports = Transaction;
