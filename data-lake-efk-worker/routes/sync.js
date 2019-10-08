const express = require('express');
const router = express.Router();
const mongodb = require('../connectors/mongodb');
const elasticsearch = require('../connectors/elasticsearch');

const INDEX_ID = 'dataLake';
const TYPE_PACKAGE = 'package';
const TYPE_FILE = 'package_file';

router.get('/list', (req, res, next) => {
    mongodb.connect()
        .then((client) => {
            client.db().collection('packages').find().toArray((err, docs) => {
                res.status(200).send(docs);
            });
        }).catch((err) => {
            res.status(500).send(err);
        });
});

router.get('/sync', (req, res, next) => {
    mongodb.connect()
        .then((client) => {
            client.db().collection('packages').find().toArray((err, docs) => {
                let body = getBulkBodyFromDocs(docs);

                //https://medium.com/@info_957/taming-elasticsearch-to-load-large-custom-json-datasets-2a2a0e31c044
                elasticsearch.client.bulk({body})
                    .then((data) => {
                        let errors = [];

                        data.items.forEach((item) => {
                            if(item.index && item.index.error) {
                                errors.append(item.index.error);
                                console.log('!!! Error indexing row ', item.index.error);
                            }
                        });

                        if(!errors.length) {
                            res.status(200);
                        }

                        else {
                            res.status(400).send(errors);
                        }
                    }).catch((err) => {
                        res.status(500).send(err);
                    });
            });
        }).catch((err) => {
        res.status(500).send(err);
    });
});

function getBulkBodyFromDocs(docs) {
    let body = [];
    let first = true;

    for(let i = 0; i < docs.length; i++) {
        let doc = docs[i];
        let files = doc.files;
        let flattenedDoc = Object.assign(doc, doc.submitter);
        delete flattenedDoc.files;
        delete flattenedDoc.submitter;

        body.push({
            _index: INDEX_ID,
            _type: TYPE_PACKAGE,
            _id: flattenedDoc._id
        });

        body.push(flattenedDoc);

        for(let j = 0; j < files.length; j++) {
            let file = files[j];

            body.push({
                _index: INDEX_ID,
                _type: TYPE_FILE,
                _id: file._id
            });

            file.packageId = doc._id;

            body.push(file);
        }

        if(first) {
            console.log('... first processed doc: ', body);
            first = false;
        }
    }

    return body;
}

module.exports = router;
