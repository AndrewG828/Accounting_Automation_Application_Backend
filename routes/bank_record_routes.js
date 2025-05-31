const multer = require('multer');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const upload = multer({ dest: 'uploads/' });
const axios = require('axios');

const express = require('express');
const router = express.Router();

const { BankRecord } = require('../models');

async function getBankRecord(bankRecordId) {
  const bankRecord = await BankRecord.findByPk(bankRecordId);
  return bankRecord || null;
}

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

router.get('/single', async (req, res) => {
  try {
    const { bankRecordId } = req.body;
    const bankRecord = getBankRecord(bankRecordId);

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

router.post('/predict', async (req, res) => {
  /**
   * In request body make sure to pass in bankRecordId.
   */
  try {
    const { bankRecordId } = req.body;
    const bankRecord = await getBankRecord(bankRecordId);

    if (!bankRecord) {
      return res.status(404).json({ message: 'Bank record not found' });
    }

    const response = await axios.post(
      'http://localhost:5001/predict',
      bankRecord.toJSON(),
    );
    const predictedCsvData = response.data.csvData;

    bankRecord.predictedCsvData = predictedCsvData;
    await bankRecord.save();

    res.json({
      message: 'Predicted data saved.',
      predictedCsvData: predictedCsvData,
    });
  } catch (error) {
    res.status(500).json({ Error: 'An error occurred', error: error.message });
  }
});

function sanitizeName(description) {
  const rawName = (description || 'Imported').split(' ')[0];
  return rawName.replace(/,/g, '').trim();
}

function generateIIF(transactions) {
  const lines = [
    '!TRNS\tTRNSTYPE\tDATE\tACCNT\tNAME\tAMOUNT\tMEMO',
    '!SPL\tTRNSTYPE\tDATE\tACCNT\tNAME\tAMOUNT\tMEMO',
    'ENDTRNS',
  ];

  transactions.forEach((t) => {
    const amount = parseFloat(t.Amount);
    const sign = t.Amount_Sign === 'negative' ? -1 : 1;
    const signedAmount = amount * sign;
    const name = sanitizeName(t.Description);

    lines.push(
      `TRNS\tGENERALJOURNAL\t${t.Date}\t${t.Account}\t${name}\t${signedAmount.toFixed(2)}\t${t.Description}`,
    );

    lines.push(
      `SPL\tGENERALJOURNAL\t${t.Date}\tBank\t${name}\t${(-signedAmount).toFixed(2)}\t${t.Description}`,
    );

    lines.push('ENDTRNS');
  });

  return lines.join('\n');
}

router.post('/export-iif', async (req, res) => {
  try {
    const { bankRecordId } = req.body;
    const bankRecord = await getBankRecord(bankRecordId);

    if (!bankRecord) {
      return res.status(404).json({ message: 'Bank record not found' });
    }
    const transactions = bankRecord.predictedCsvData;

    const iifContent = generateIIF(transactions);

    // Create temp file (or stream directly)
    const tempPath = path.join(__dirname, 'output.iif');
    fs.writeFileSync(tempPath, iifContent);

    // Send as downloadable attachment
    res.download(tempPath, 'export.iif', (err) => {
      if (err) {
        console.error('Error sending IIF:', err);
        res.status(500).send('Failed to export IIF');
      } else {
        fs.unlink(tempPath, () => {});
      }
    });
  } catch (error) {
    console.error('Export error:', error);
    res
      .status(500)
      .json({ message: 'Failed to generate IIF', error: error.message });
  }
});
// router.post('/export-iif', async (req, res) => {
//   try {
//     const { bankRecordId } = req.body;
//     const bankRecord = await getBankRecord(bankRecordId);

//     if (!bankRecord) {
//       return res.status(404).json({ message: 'Bank record not found' });
//     }

//     const transactions = bankRecord.predictedCsvData;

//     if (!Array.isArray(transactions) || transactions.length === 0) {
//       return res
//         .status(400)
//         .json({ message: 'No predictedCsvData found or it is empty.' });
//     }

//     const iifContent = generateIIF(transactions);

//     // Set headers for download or inline view
//     res.setHeader('Content-Disposition', 'attachment; filename="export.iif"');
//     res.setHeader('Content-Type', 'text/plain');

//     res.send(iifContent);
//   } catch (error) {
//     console.error('Export error:', error);
//     res.status(500).json({ message: 'Failed to generate IIF', error });
//   }
// });

module.exports = router;
