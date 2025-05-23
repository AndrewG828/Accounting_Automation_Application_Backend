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
        type: DataTypes.JSONB,
        allowNull: false,
      },
      uploadedAt: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW,
      },
      sortCsvData: {
        type: DataTypes.JSONB,
        allowNull: true,
      },
    },
    {
      underscored: true,
    },
  );
};
