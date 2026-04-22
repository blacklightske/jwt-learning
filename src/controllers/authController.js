const jwt = require('jsonwebtoken');
const { SECRET_KEY } = require('../config/jwt');

const createToken = (req, res) => {
  const payload = {
    sub: '12345',
    email: 'george@example.com',
    role: 'admin',
  };

  const token = jwt.sign(payload, SECRET_KEY, { expiresIn: '1h' });

  res.json({
    message: 'Token created',
    token,
  });
};

module.exports = {
  createToken,
};