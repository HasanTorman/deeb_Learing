const moment = require('moment');

const getCurrentTimestamp = () => {
  return moment().toDate();
};

module.exports = {
  getCurrentTimestamp
};
