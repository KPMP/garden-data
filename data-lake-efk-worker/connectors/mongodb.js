const Client = require('mongodb').MongoClient;

module.exports = { connect: () => Client.connect(process.env.ENV_MONGO_URL) };
