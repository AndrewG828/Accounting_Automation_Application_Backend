const express = require('express');
const router = express.Router();

const userRoutes = require('./user_routes');

router.use('/user', userRoutes);

router.get('/', (req, res) => {
  res.send('Testing');
});

module.exports = router;
