const express = require('express');
const router = express.Router();
const {
  getNews,
  createNews,
  updateNews,
  deleteNews
} = require('../controllers/newsController');
const { auth, adminAuth } = require('../middleware/auth');

router.get('/', auth, getNews);
router.post('/', auth, adminAuth, createNews);
router.put('/:id', auth, adminAuth, updateNews);
router.delete('/:id', auth, adminAuth, deleteNews);

module.exports = router;
