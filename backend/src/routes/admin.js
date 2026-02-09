const express = require('express');
const router = express.Router();
const {
  getAdmins,
  createAdmin,
  updateAdmin,
  deleteAdmin
} = require('../controllers/adminController');
const { auth, adminAuth } = require('../middleware/auth');

router.get('/', auth, adminAuth, getAdmins);
router.post('/', auth, adminAuth, createAdmin);
router.put('/:id', auth, adminAuth, updateAdmin);
router.delete('/:id', auth, adminAuth, deleteAdmin);

module.exports = router;
