module.exports = (sequelize, DataTypes) => {
  return sequelize.define(
    'User',
    {
      userId: {
        type: DataTypes.INTEGER,
        allowNull: false,
        primaryKey: true,
        autoIncrement: true,
      },
      username: {
        type: DataTypes.STRING(50),
        unique: true,
        allowNull: false,
      },
      email: {
        type: DataTypes.STRING(100),
        unique: true,
        allowNull: true,
      },
      hashedPassword: {
        type: DataTypes.STRING(255),
        allowNull: false,
      },
    },
    {
      underscored: true,
    },
  );
};
