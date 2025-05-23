require('dotenv').config();

const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

const { sequelize } = require('./models');

const routes = require('./routes');
app.use('/api', routes);

const PORT = process.env.PORT || 8001;

sequelize
  .sync({ force: false, alter: true })
  .then(() => {
    console.log('database synced');
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  })
  .catch((err) => {
    console.log('Unable to connect to the database', err);
  });
