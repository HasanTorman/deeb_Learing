const { DataTypes, Model } = require('sequelize');
const sequelize = require('../index');

class Employee extends Model { }

Employee.init({
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  }
}, { sequelize, modelName: 'availableIp', tableName: 'available_ips', timestamps: false });

module.exports = Employee;

