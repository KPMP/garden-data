const { Client } = require('@elastic/elasticsearch');

module.exports = { client: new Client({node: process.env.ENV_ELASTICSEARCH_URL}) };
