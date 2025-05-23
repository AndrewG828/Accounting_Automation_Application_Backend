const express = require('express');
const user = require('../models/user');
const router = express.Router();

const { Client } = require('../models');

router.post('/create', (req, res) => {
  try {
    const { clientName, userId } = req.body;

    if (!clientName || !userId) {
      return res.status(400).send('clientName and userId are required!');
    }

    Client.create({
      clientName: clientName,
      userId: userId,
    });

    res.send('Client created successfully.');
  } catch (error) {
    res.status(500).send('Error creating client.');
  }
});

module.exports = router;
