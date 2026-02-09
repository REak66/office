const express = require('express');
const router = express.Router();
const {
  getCirculars,
  createCircular,
  updateCircular,
  deleteCircular
} = require('../controllers/circularController');
const { auth, adminAuth } = require('../middleware/auth');

router.get('/', auth, getCirculars);
router.post('/', auth, adminAuth, createCircular);
router.put('/:id', auth, adminAuth, updateCircular);
router.delete('/:id', auth, adminAuth, deleteCircular);

module.exports = router;
