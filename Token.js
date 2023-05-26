const { v4: uuidv4 } = require('uuid');

class Token {
  constructor() {
    const uuid = uuidv4();
    const formattedUUID = `${uuid.substr(0, 8)}-${uuid.substr(8, 4)}-${uuid.substr(12, 4)}-${uuid.substr(16, 4)}-${uuid.substr(20)}`;
    this.id = `TKN ${formattedUUID}`;
  }

  toString() {
    return this.id;
  }
}

module.exports = Token;

