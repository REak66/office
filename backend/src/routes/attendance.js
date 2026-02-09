const express = require('express');
const router = express.Router();
const {
  getAttendance,
  createAttendance,
  updateAttendance,
  deleteAttendance
} = require('../controllers/attendanceController');
const { auth, adminAuth } = require('../middleware/auth');

router.get('/', auth, getAttendance);
router.post('/', auth, createAttendance);
router.put('/:id', auth, updateAttendance);
router.delete('/:id', auth, adminAuth, deleteAttendance);

module.exports = router;
