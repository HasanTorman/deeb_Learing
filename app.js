const { initializeDatabase } = require('./utils/database');
const { logAttempt } = require('./services/activationService');

const main = async () => {
  await initializeDatabase();

  // Example of logging an attempt
  logAttempt('emp123', 'emu456', '192.168.1.1', '1234567890', 'US', 'success', '', 'mobile', 'android_10');
};

main();
