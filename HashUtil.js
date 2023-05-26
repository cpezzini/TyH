
const crypto = require('crypto');
let currentAlgorithm = 'sha256';

function generateHash(block) {
  const { timestamp, transactions, previousHash } = block;
  const timestampString = timestamp ? timestamp.toString() : '';
  const transactionsString = transactions ? JSON.stringify(transactions) : '';
  const previousHashString = previousHash ? previousHash.toString() : '';

  const data = [timestampString, transactionsString, previousHashString].join('');
  const hash = crypto.createHash(currentAlgorithm);
  hash.update(data);
  const generatedHash = hash.digest('hex');

  // Cambiar algoritmo para la próxima generación de hash
  currentAlgorithm = (currentAlgorithm === 'sha256') ? 'md5' : 'sha256';

  return generatedHash;
}

module.exports = { generateHash };
