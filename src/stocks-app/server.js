const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();

app.use(cookieParser());

app.get('/api/logout', (req, res) => {
    res.clearCookie('session-token');
    res.redirect('/');
});

app.listen(5000, () => {
    console.log('Server is running on port 5000');
});