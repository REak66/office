const express = require('express');
const router = express.Router();
const {
  getDocuments,
  createDocument,
  updateDocument,
  deleteDocument
} = require('../controllers/documentController');
const { auth, adminAuth } = require('../middleware/auth');

router.get('/', auth, getDocuments);
router.post('/', auth, createDocument);
router.put('/:id', auth, updateDocument);
router.delete('/:id', auth, adminAuth, deleteDocument);

module.exports = router;
