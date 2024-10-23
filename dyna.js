const express = require('express');
const QRCode = require('qrcode');

const app = express();

app.get('/generate-qr/:data', (req, res) => {
    const data = req.params.data;

    // Generate QR code
    QRCode.toDataURL(data, function (err, url) {
        if (err) res.send('Error occurred');

        // Send QR code image
        res.send(`<img src="${url}" alt="QR Code" />`);
    });
});

app.get('/dynamic-link', (req, res) => {
    // This could be a dynamic link, for example, based on database content
    res.redirect('https://www.example.com');
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
