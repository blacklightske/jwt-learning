const express = require('express');
const router = express.Router();

const { createToken } = require('../controllers/authController');
const authMiddleware = require('../middleware/authMiddleware');

router.get('/token', createToken);

router.get('/protected', authMiddleware, (req, res) => {
  res.json({
    message: 'Protected route',
    user: req.user,
  });
});

module.exports = router;