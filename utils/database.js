const sequelize = require('../database');
const User = require('../database/models/users');
const Activation = require('../database/models/activation');

const initializeDatabase = async () => {
    await sequelize.sync();
};

module.exports = {
    User,
    Activation,
    initializeDatabase
};
