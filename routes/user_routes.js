const bcrypt = require('bcrypt');

const express = require('express');
const router = express.Router();

const { User, Client } = require('../models');

async function registerUser(req, res) {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      res.status(400).json({ error: 'Username and password are require!' });
    }

    const hashedPassword = await bcrypt.hash(password, 25);

    User.create({ username: username, hashedPassword: hashedPassword });

    res.status(201).send(`User ${username} successfully register.`);
  } catch (error) {
    res.status(500).send('Error registering user.');
  }
}

async function logInUser(req, res) {
  try {
    const { username, password } = req.body;

    const user = await User.findOne({ where: { username: username } });

    if (!user) {
      res.status(404).send('Invalid username or password');
    }

    const match = await bcrypt.compare(password, user.hashedPassword);

    if (match) {
      res.send('Login successful.');
    } else {
      res.status(400).send('Invalid password.');
    }
  } catch (error) {
    res.status(500).send('Error logging in');
  }
}

router.get('/users', async (req, res) => {
  try {
    const users = await User.findAll();
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.post('/register', async (req, res) => {
  registerUser(req, res);
});

router.post('/login', async (req, res) => {
  logInUser(req, res);
});

module.exports = router;
