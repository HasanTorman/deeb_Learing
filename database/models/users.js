const { DataTypes, Model } = require('sequelize');
const sequelize = require('../index');

class Employee extends Model { }

Employee.init({
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
  }
}, { sequelize, modelName: 'user', tableName: 'users', timestamps: false });

module.exports = Employee;
