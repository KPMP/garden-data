const express = require('express');
const router = express.Router();
const mongodb = require('../connectors/mongodb');
const elasticsearch = require('../connectors/elasticsearch');

const TYPE_PACKAGE = 'packages';
const TYPE_FILE = 'package_files';

router.get('/list-datalake', (req, res, next) => {
    mongodb.connect()
        .then((client) => {
            client.db().collection('packages').find().toArray((err, docs) => {
                res.status(200).send(docs);
            });
        }).catch((err) => {
            console.error('!!! Error connecting to mongodb: ', err);
            res.status(500).send(err);
        });
});

router.get('/list-es-packages', (req, res, next) => {
    elasticsearch.client.search({
            index: TYPE_PACKAGE
        }).then((data) => {
            res.status(200).send(data);
        }).catch((err) => {
        console.error('!!! Error connecting to elasticsearch: ', err);
        res.status(500).send(err);
    });
});

router.get('/list-es-files', (req, res, next) => {
    elasticsearch.client.search({
        index: TYPE_FILE
    }).then((data) => {
        res.status(200).send(data);
    }).catch((err) => {
        console.error('!!! Error connecting to elasticsearch: ', err);
        res.status(500).send(err);
    });
});

router.get('/sync', (req, res, next) => {
    mongodb.connect()
        .then((client) => {
            client.db().collection('packages').find().toArray((err, docs) => {
                let body = getElasticsearchBulkBodyFromMongoResponse(docs);

                //https://medium.com/@info_957/taming-elasticsearch-to-load-large-custom-json-datasets-2a2a0e31c044
                elasticsearch.client.bulk({
                    body: body
                }).then((data) => {
                    let errors = [];

                    //Check bulk API response, item by item, for errors; respond accordingly
                    data.body.items.forEach((item) => {
                        if(item.index && item.index.error) {
                            errors.push(item.index.error);
                        }
                    });

                    if(!errors.length) {
                        res.status(200).send(data);
                    }

                    else {
                        res.status(400).send(errors);
                    }
                }).catch((err) => {
                    console.error('!!! Error connecting to elasticsearch: ', err);
                    res.status(500).send(err);
                });
            });
        }).catch((err) => {
        console.error('!!! Error connecting to mongodb: ', err);
        res.status(500).send(err);
    });
});

function getElasticsearchBulkBodyFromMongoResponse(docs) {
    let body = [];

    for(let i = 0; i < docs.length; i++) {
        let doc = docs[i];
        let packageId = doc._id;
        let files = doc.files;
        let flatPackage = Object.assign(doc, doc.submitter);
        delete flatPackage.files;
        delete flatPackage.submitter;
        delete flatPackage._id;

        body.push({
            update: {
                _index: TYPE_PACKAGE,
                _type: TYPE_PACKAGE,
                _id: packageId
            }
        });

        body.push({
            doc: flatPackage,
            doc_as_upsert: true
        });

        for(let j = 0; j < files.length; j++) {
            let file = files[j];
            let fileId = file._id;
            file.packageId = packageId;
            delete file._id;

            body.push({
                update: {
                    _index: TYPE_FILE,
                    _type: TYPE_FILE,
                    _id: fileId
                }
            });


            body.push({
                doc: file,
                doc_as_upsert: true
            });
        }
    }

    return body;
}

module.exports = router;
