const { DataTypes, Model } = require('sequelize');
const sequelize = require('../index');

class IpLimit extends Model { }

IpLimit.init({
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    activation_count: {
        type: DataTypes.INTEGER,
        defaultValue: 0
    },
    max_activations: {
        type: DataTypes.INTEGER,
        defaultValue: 4
    },
    time_window_start: {
        type: DataTypes.DATE
    },
    time_window_end: {
        type: DataTypes.DATE
    }
}, { sequelize, modelName: 'ipLimit', tableName: 'ip_limits', timestamps: false });

module.exports = IpLimit;
