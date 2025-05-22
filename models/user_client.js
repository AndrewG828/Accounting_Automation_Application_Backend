module.exports = (sequelize, DataTypes) => {
  return sequelize.define(
    'UserClient',
    {
      userId: {
        type: DataTypes.INTEGER,
        allowNull: false,
      },
      clientId: {
        type: DataTypes.INTEGER,
        allowNull: false,
      },
    },
    {
      underscored: true,
    },
  );
};
