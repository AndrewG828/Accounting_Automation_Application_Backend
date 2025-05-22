module.exports = (sequelize, DataTypes) => {
  return sequelize.define(
    'BankRecord',
    {
      bankRecordId: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true,
      },
      clientId: {
        type: DataTypes.INTEGER,
        unique: true,
        allowNull: false,
      },
      csvData: {
        type: DataTypes.TEXT,
        allowNull: false,
      },
      sortCsvData: {
        type: DataTypes.TEXT,
        allowNull: true,
      },
    },
    {
      underscored: true,
    },
  );
};
