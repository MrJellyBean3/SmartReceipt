const express = require('express');
const multer  = require('multer');
const fs = require('fs');
const path = require('path');

// Setup Express app
const app = express();

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Serve static files from the 'uploads' and 'graph-dir' directories
app.use('/uploads', express.static('uploads'));
app.use('/graph-dir', express.static('graph-dir'));

// Configure multer to store uploaded files in 'uploads' directory
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/')
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname)
    }
});

const upload = multer({ storage: storage });

// Route to upload files
app.post('/upload', upload.single('file'), (req, res) => {
    if (!req.file) {
        return res.status(400).send('No files were uploaded.');
    }
    // Send the path of the uploaded file
    res.send({ path: `/uploads/${req.file.filename}` });
});

// Route to check if file exists
app.get('/check-file', (req, res) => {
    const filePath = path.join(__dirname, 'graph-dir', 'graph.PNG');
    fs.access(filePath, fs.constants.F_OK, (err) => {
        res.send({ fileExists: !err });
    });
});

// Start the server on port 3000
app.listen(3000, "192.168.1.30",() => console.log('Server started on port 3000. the link is: \nhttp://192.168.1.30:3000/'));
