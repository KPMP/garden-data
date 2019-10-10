# EFK Integration with the Data Lake

## Running
1. `cd garden-data/data-lake-efk-worker && cp .env.example .env`
2. Set ENV_NODE_APPDIR to your local `garden-data/data-lake-efk-worker` directory
3. Make sure your `heavens-docker` project is up-to-date with ticket KPMP-1296
4. Raise projects in order
 * `cd heavens-docker/ara && docker-compose up -d`
 * `cd heavens-docker/orion && docker-compose -f docker-compose.dev.yml up -d`
 * `cd garden-data/data-lake-efk-worker && docker-compose up -d`

## Testing
 * `http://localhost:5000/list-datalake` : show all packages in your dataLake mongodb
 * `http://localhost:5000/list-es-packages` : show all, if any, packages in Elasticsearch
 * `http://localhost:5000/list-es-files` : show all, if any, package files in Elasticsearch (linked to parent packages by package_id)
 * `http://localhost:5000/sync` : idempotent sync all documents in `dataLake.packages` to Elasticsearch `packages` and `package_files` indexes

## Development Notes
 - Mongodb with node
   - [mongodb native client for node](https://github.com/mongodb/node-mongodb-native)
 - Elasticsearch with node
   - [Elasticsearch JS for node](https://github.com/elastic/elasticsearch-js)
   - [Elasticsearch node API main reference](https://www.elastic.co/guide/en/elasticsearch/client/javascript-api/current/api-reference.html)
   - [Taming elasticsearch in node, medium](https://medium.com/@info_957/taming-elasticsearch-to-load-large-custom-json-datasets-2a2a0e31c044)
   - [Bulk update, doc_as_upsert with node API](https://www.elastic.co/guide/en/elasticsearch/reference/7.1/docs-bulk.html)
