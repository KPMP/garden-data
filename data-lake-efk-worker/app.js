const express = require('express');
const syncRouter = require('./routes/sync');
const app = express();

app.use('/', syncRouter);
app.listen(process.env.ENV_EXPRESS_PORT || 5000);
