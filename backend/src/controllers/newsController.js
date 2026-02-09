const News = require('../models/News');

// @desc    Get all news
// @route   GET /api/news
// @access  Private
exports.getNews = async (req, res) => {
  try {
    const news = await News.find()
      .populate('author', 'name email')
      .sort({ publishedDate: -1 });
    res.json(news);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Create news article
// @route   POST /api/news
// @access  Private/Admin
exports.createNews = async (req, res) => {
  try {
    const { title, content, publishedDate } = req.body;
    const news = await News.create({
      title,
      content,
      author: req.user._id,
      publishedDate
    });
    const populatedNews = await News.findById(news._id).populate('author', 'name email');
    res.status(201).json(populatedNews);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Update news article
// @route   PUT /api/news/:id
// @access  Private/Admin
exports.updateNews = async (req, res) => {
  try {
    const news = await News.findByIdAndUpdate(req.params.id, req.body, { new: true })
      .populate('author', 'name email');
    if (!news) {
      return res.status(404).json({ message: 'News article not found' });
    }
    res.json(news);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Delete news article
// @route   DELETE /api/news/:id
// @access  Private/Admin
exports.deleteNews = async (req, res) => {
  try {
    const news = await News.findByIdAndDelete(req.params.id);
    if (!news) {
      return res.status(404).json({ message: 'News article not found' });
    }
    res.json({ message: 'News article removed' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
