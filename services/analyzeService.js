const { spawn } = require('child_process');
const sequelize = require('../database/index');

async function getActivations() {
    const result = await sequelize.query('SELECT * FROM activations', { type: sequelize.QueryTypes.SELECT });
    return result;
}

async function analyzeData() {
    const activations = await getActivations();
    const py = spawn('python', ['services/analyze.py']);
    py.stdin.write(JSON.stringify(activations));
    py.stdin.end();

    py.stdout.on('data', (data) => {
        console.log(`Analysis Result: ${data}`);
    });

    py.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
    });
}

module.exports = {
    analyzeData
};
