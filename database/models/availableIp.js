const { DataTypes, Model } = require('sequelize');
const sequelize = require('../index');

class AvailableIp extends Model {}

AvailableIp.init({
  ip: {
    type: DataTypes.STRING(255),
    primaryKey: true
  }
}, {
  sequelize,
  modelName: 'available_ip',
  tableName: 'available_ips',
  timestamps: false
});

module.exports = AvailableIp;
