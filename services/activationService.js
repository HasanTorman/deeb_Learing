const { Activation } = require('../utils/database');
const { getCurrentTimestamp } = require('../utils/timestamp');

const logAttempt = async (user_id, emulator_id, ip, phone_number, country_code, result, error_message, device_type, os_version) => {
  try {
    await Activation.create({
      user_id,
      emulator_id,
      ip,
      phone_number,
      country_code,
      result,
      error_message,
      device_type,
      os_version,
      timestamp: getCurrentTimestamp()
    });
    console.log('Data logged successfully');
  } catch (error) {
    console.error('Error logging data:', error);
  }
};

module.exports = {
  logAttempt
};
