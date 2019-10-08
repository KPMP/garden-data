const express = require('express');
const syncRouter = require('./routes/sync');
const app = express();

app.use('/', syncRouter);

app.listen(5050);
