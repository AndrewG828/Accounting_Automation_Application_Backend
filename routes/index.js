const express = require('express');
const router = express.Router();

const userRoutes = require('./user_routes');
const clientRoutes = require('./client_routes');
const bankRecordRoutes = require('./bank_record_routes');

router.use('/user', userRoutes);
router.use('/client', clientRoutes);
router.use('/bank-record', bankRecordRoutes);

router.get('/', (req, res) => {
  res.send('Testing');
});

module.exports = router;
