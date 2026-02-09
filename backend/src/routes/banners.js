const express = require('express');
const router = express.Router();
const {
  getBanners,
  createBanner,
  updateBanner,
  deleteBanner
} = require('../controllers/bannerController');
const { auth, adminAuth } = require('../middleware/auth');

router.get('/', auth, getBanners);
router.post('/', auth, adminAuth, createBanner);
router.put('/:id', auth, adminAuth, updateBanner);
router.delete('/:id', auth, adminAuth, deleteBanner);

module.exports = router;
