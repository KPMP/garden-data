const Client = require('mongodb').MongoClient;

const url = 'mongodb://localhost:27017/dataLake';

function connect() {
    return Client.connect(url);
}

module.exports = { connect };
