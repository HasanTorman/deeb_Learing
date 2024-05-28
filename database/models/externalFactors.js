const { DataTypes, Model } = require('sequelize');
const sequelize = require('../index');

class ExternalFactor extends Model { }

const ExternalFactor = sequelize.define('ExternalFactor', {
    factor_type: {
      type: DataTypes.STRING,
      allowNull: false
    },
    description: {
      type: DataTypes.TEXT,
      allowNull: false
    },
    date: {
      type: DataTypes.DATE,
      allowNull: false
    }
  }, {
    sequelize,
    tableName: 'external_factors',
    timestamps: false
  });

  module.exports = ExternalFactor;
