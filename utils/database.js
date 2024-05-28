const sequelize = require('../database');
const User = require('../database/models/users');
const Activation = require('../database/models/activation');
const AvailableIp = require('../database/models/availableIp');
const IpLimit = require('../database/models/ipLimit');
const UsedPhoneNumbers = require('../database/models/usedPhoneNumber');

const initializeDatabase = async () => {
    await sequelize.sync();
};

module.exports = {
    User,
    Activation,
    AvailableIp,
    IpLimit,
    UsedPhoneNumbers,
    initializeDatabase
};
