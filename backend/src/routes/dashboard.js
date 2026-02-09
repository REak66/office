const express = require('express');
const router = express.Router();
const {
  getSummary,
  getAttendanceSummary,
  getDocumentSubmission
} = require('../controllers/dashboardController');
const { auth } = require('../middleware/auth');

router.get('/summary', auth, getSummary);
router.get('/attendance-summary', auth, getAttendanceSummary);
router.get('/document-submission', auth, getDocumentSubmission);

module.exports = router;
