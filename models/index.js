const { Sequelize, DataTypes } = require('sequelize');
const UserModel = require('./user');
const config = require('../config/config');

const sequelize = new Sequelize(config.development);

const User = UserModel(sequelize, DataTypes);

module.exports = {
  sequelize,
  User,
};
