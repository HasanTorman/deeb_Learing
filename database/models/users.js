const { DataTypes, Model } = require('sequelize');
const sequelize = require('../index');

class User extends Model { }

User.init({
  user_id: {
    type: DataTypes.STRING(255),
    allowNull: false
  },
  emulator_id: {
    type: DataTypes.STRING,
    allowNull: false
  }
}, { sequelize, modelName: 'user', tableName: 'users', timestamps: false });

module.exports = User;
