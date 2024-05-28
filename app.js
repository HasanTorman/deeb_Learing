const express = require('express');
const { analyzeData } = require('./services/analyzeService');
const { Activation, AvailableIp } = require('./utils/database');
const pug = require('pug');
const { initializeDatabase } = require('./utils/database');
const { logAttempt } = require('./services/activationService');
const { Op } = require('sequelize');
const moment = require('moment');


const main = async () => {
  await initializeDatabase();
  // Example of logging an attempt
  logAttempt('emp123', 'emu456', '192.168.1.1', '1234567890', 'US', 'success', '', 'mobile', 'android_10');
};

// main();

const app = express();


app.set('view engine', 'pug');

app.get('/api/activations', async (req, res) => {
  const activations = await Activation.findAll();
  res.json(activations);
  // res.render('dashboard', { activations });
});

app.get('/analyze', async (req, res) => {
  await analyzeData();
  res.send('Analysis complete. Check console for results.');
});

app.get('/api/unused-ips', async (req, res) => {
  try {
    const usedIps = await Activation.findAll({
      attributes: ['ip'],
      group: ['ip']
    });
    const usedIpAddresses = usedIps.map(ip => ip.ip);

    const unusedIps = await AvailableIp.findAll({
      where: {
        ip: {
          [Op.notIn]: usedIpAddresses
        }
      }
    });

    res.json(unusedIps);
  } catch (error) {
    res.status(500).send(error.message);
  }
});

app.get('/api/analyze-ip-limits', async (req, res) => {
  try {
    const startTime = moment().subtract(82, 'hours').toDate();
    const endTime = new Date();

    console.log(startTime, endTime);

    const attempts = await Activation.findAll({
      where: {
        timestamp: {
          [Op.between]: [startTime, endTime]
        }
      }
    });


    const ipAttempts = attempts.reduce((acc, attempt) => {
      const ip = attempt.ip;
      if (!acc[ip]) {
        acc[ip] = { success: 0, fail: 0 };
      }
      if (attempt.result === 'success') {
        acc[ip].success += 1;
      } else {
        acc[ip].fail += 1;
      }
      return acc;
    }, {});

    res.json(ipAttempts);
  } catch (error) {
    res.status(500).send(error.message);
  }
});
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});






