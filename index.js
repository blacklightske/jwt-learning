const express = require('express');
const jwt = require('jsonwebtoken');

const app = express();
app.use(express.json());

const SECRET_KEY = 'my_super_secret_key';

app.get('/', (req, res) => {
  res.send('JWT practice server running');
});

app.get('/create-token', (req, res) => {
  const payload = {
    sub: '12345',
    email: 'george@example.com',
    role: 'admin',
  };

  const token = jwt.sign(payload, SECRET_KEY, { expiresIn: '1h' });

  res.json({
    message: 'Token created successfully',
    token,
  });
});

app.get('/public', (req, res) => {
  res.json({ message: 'This is a public route' });
});

function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;

  // 1. Check if header exists
  if (!authHeader) {
    return res.status(401).json({ message: 'No token provided' });
  }

  // 2. Extract token
  const token = authHeader.split(' ')[1];

  try {
    // 3. Verify token
    const decoded = jwt.verify(token, SECRET_KEY);

    // 4. Attach user data to request
    req.user = decoded;

    // 5. Allow request to continue
    next();
  } catch (error) {
    return res.status(401).json({ message: 'Invalid token' });
  }
}

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});