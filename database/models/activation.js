const { DataTypes, Model } = require('sequelize');
const sequelize = require('../index');

class Activation extends Model { }

Activation.init({
  user_id: {
    type: DataTypes.STRING,
    allowNull: false
  },
  emulator_id: {
    type: DataTypes.STRING,
    allowNull: false
  },
  ip: {
    type: DataTypes.STRING,
    allowNull: false
  },
  phone_number: {
    type: DataTypes.STRING,
    allowNull: false
  },
  country_code: {
    type: DataTypes.STRING
  },
  city: {
    type: DataTypes.STRING
  },
  country: {
    type: DataTypes.STRING
  },
  vpn_provider: {
    type: DataTypes.STRING
  },
  sms_provider: {
    type: DataTypes.STRING,
    defaultValue: 'SMS Activate'
  },
  result: {
    type: DataTypes.STRING
  },
  error_message: {
    type: DataTypes.STRING
  },
  device_type: {
    type: DataTypes.STRING
  },
  os_version: {
    type: DataTypes.STRING
  },
  timestamp: {
    type: DataTypes.DATE  // Time of activation attempt
  },
  emulator_time: {
    type: DataTypes.DATE  // Time on emulator
  },
  activation_country_time: {
    type: DataTypes.DATE  // Time in activation country
  },
  vpn_country_time: {
    type: DataTypes.DATE  // Time in VPN country
  },
  failure_reason: {
    type: DataTypes.STRING  // Field to store failure reason
  },
  cost: {
    type: DataTypes.DECIMAL(10, 2),
    defaultValue: 0.00
  }
}, {
  sequelize,
  modelName: 'activation',
  tableName: 'activations',
  timestamps: false
});

module.exports = Activation;
