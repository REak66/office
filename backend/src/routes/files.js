const express = require('express');
const router = express.Router();
const {
  uploadFile,
  getFiles,
  downloadFile,
  deleteFile
} = require('../controllers/fileController');
const { auth, adminAuth } = require('../middleware/auth');

router.post('/upload', auth, uploadFile);
router.get('/', auth, getFiles);
router.get('/:id/download', auth, downloadFile);
router.delete('/:id', auth, adminAuth, deleteFile);

module.exports = router;
