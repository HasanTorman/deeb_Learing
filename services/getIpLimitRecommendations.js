const { sequelize, Activation } = require('../models');
const { Op } = require('sequelize');
const moment = require('moment');

async function analyzeIpLimits() {
  const startTime = moment().subtract(1, 'hours').toDate();
  const endTime = new Date();

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

  return ipAttempts;
}

analyzeIpLimits().then(ipAttempts => {
  console.log(ipAttempts);
});

async function getIpLimitRecommendations() {
    const attempts = await analyzeIpLimits();
    
    // افتراض أن لدينا نموذج تم تدريبه على تحديد الحد الأقصى للمحاولات
    const rfModel = loadRandomForestModel(); // الدالة لتحميل النموذج المدرب
  
    const ipLimits = {};
  
    for (const ip in attempts) {
      const { success, fail } = attempts[ip];
      const totalAttempts = success + fail;
  
      // توقع الحد الأقصى باستخدام النموذج المدرب
      const predictedLimit = rfModel.predict([[ip, totalAttempts]])[0];
      ipLimits[ip] = predictedLimit;
    }
  
    return ipLimits;
  }
  
  getIpLimitRecommendations().then(ipLimits => {
    console.log('Recommended IP Limits:', ipLimits);
  });
  