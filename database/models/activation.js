const { DataTypes, Model } = require('sequelize');
const sequelize = require('../index');

class Activation extends Model { }

Activation.init({
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  user_id: {
    type: DataTypes.STRING(255),
    allowNull: false
  },
  emulator_id: {
    type: DataTypes.STRING(255),
    allowNull: false
  },
  ip: {
    type: DataTypes.STRING(255),
    allowNull: false
  },
  phone_number: {
    type: DataTypes.STRING(255),
    allowNull: false
  },
  country_code: {
    type: DataTypes.STRING(50)
  },
  result: {
    type: DataTypes.STRING(50)
  },
  error_message: {
    type: DataTypes.STRING(255)
  },
  device_type: {
    type: DataTypes.STRING(255)
  },
  os_version: {
    type: DataTypes.STRING(50)
  },
  timestamp: {
    type: DataTypes.DATE,
    allowNull: false,
    defaultValue: DataTypes.NOW
  }
}, { sequelize, modelName: 'activation', tableName: 'activations', timestamps: false });

module.exports = Activation;
