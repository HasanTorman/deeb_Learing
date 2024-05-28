const { DataTypes, Model } = require('sequelize');
const sequelize = require('../index');

class UsedPhoneNumber extends Model { }

UsedPhoneNumber.init({
    phone_number: {
        type: DataTypes.STRING,
        unique: true,
        allowNull: false
    },
    cost: {
        type: DataTypes.DECIMAL(10, 2),
        defaultValue: 0.00
    }
}, {
    sequelize,
    modelName: 'UsedPhoneNumber',
    tableName: 'used_phone_numbers',
    timestamps: false
});

module.exports = UsedPhoneNumber;

