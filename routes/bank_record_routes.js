const multer = require('multer');
const fs = require('fs');
const csv = require('csv-parser');
const upload = multer({ dest: 'uploads/' });

const express = require('express');
const router = express.Router();

const { BankRecord } = require('../models');

router.get('/all', async (req, res) => {
  try {
    const bankRecords = await BankRecord.findAll();

    if (!bankRecords || bankRecords.length === 0) {
      return res.status(404).json({ message: 'No bank records found.' });
    }

    res.json(bankRecords);
  } catch (error) {
    console.error('Error fetching all bank records:', error);
    res.status(500).json({
      message: 'An error occurred while getting all bank records.',
      error,
    });
  }
});

router.get('/:id', async (req, res) => {
  try {
    const bankRecord = await BankRecord.findByPk(req.params.id);

    if (!bankRecord) {
      return res.status(404).json({ message: 'Bank record not found' });
    }

    res.json(bankRecord);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching bank record', error });
  }
});

router.post('/upload', upload.single('csvFile'), async (req, res) => {
  const results = [];

  fs.createReadStream(req.file.path)
    .pipe(csv())
    .on('data', (data) => results.push(data))
    .on('end', async () => {
      try {
        await BankRecord.create({
          clientId: req.body.clientId,
          csvData: results, // Store JSON array
        });

        res.json(results);
      } catch (err) {
        console.error(err);
        res.status(500).send('Error saving CSV data');
      }
    });
});

module.exports = router;
