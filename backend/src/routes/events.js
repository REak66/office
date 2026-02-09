const express = require('express');
const router = express.Router();
const {
  getEvents,
  createEvent,
  updateEvent,
  deleteEvent
} = require('../controllers/eventController');
const { auth, adminAuth } = require('../middleware/auth');

router.get('/', auth, getEvents);
router.post('/', auth, adminAuth, createEvent);
router.put('/:id', auth, adminAuth, updateEvent);
router.delete('/:id', auth, adminAuth, deleteEvent);

module.exports = router;
