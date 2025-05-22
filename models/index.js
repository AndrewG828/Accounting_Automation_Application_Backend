const { Sequelize, DataTypes } = require('sequelize');
const config = require('../config/config');

const sequelize = new Sequelize(config.development);

const UserModel = require('./user');
const ClientModel = require('./client');
const BankRecordModel = require('./bank_record');
const UserClientModel = require('./user_client');

const User = UserModel(sequelize, DataTypes);
const Client = ClientModel(sequelize, DataTypes);
const BankRecord = BankRecordModel(sequelize, DataTypes);
const UserClient = UserClientModel(sequelize, DataTypes);

User.belongsToMany(Client, { through: UserClient, foreignKey: 'userId' });
Client.belongsToMany(User, { through: UserClient, foreignKey: 'clientId' });

Client.hasMany(BankRecord, { foreignKey: 'clientId' });
BankRecord.belongsTo(Client, { foreignKey: 'clientId' });

module.exports = {
  sequelize,
  User,
  Client,
  BankRecord,
};
