const CircularLetter = require('../models/CircularLetter');

// @desc    Get all circular letters
// @route   GET /api/circulars
// @access  Private
exports.getCirculars = async (req, res) => {
  try {
    const { page = 1, limit = 10, priority } = req.query;
    const skip = (page - 1) * limit;

    let query = {};
    if (priority) query.priority = priority;

    const circulars = await CircularLetter.find(query)
      .populate('createdBy', 'name email')
      .limit(parseInt(limit))
      .skip(skip)
      .sort({ createdAt: -1 });

    const total = await CircularLetter.countDocuments(query);

    res.json({
      circulars,
      currentPage: parseInt(page),
      totalPages: Math.ceil(total / limit),
      total
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Create circular letter
// @route   POST /api/circulars
// @access  Private/Admin
exports.createCircular = async (req, res) => {
  try {
    const { title, referenceNumber, priority, content, date } = req.body;

    const circular = await CircularLetter.create({
      title,
      referenceNumber,
      priority,
      content,
      date,
      createdBy: req.user._id
    });

    const populatedCircular = await CircularLetter.findById(circular._id)
      .populate('createdBy', 'name email');

    res.status(201).json(populatedCircular);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Update circular letter
// @route   PUT /api/circulars/:id
// @access  Private/Admin
exports.updateCircular = async (req, res) => {
  try {
    const circular = await CircularLetter.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true, runValidators: true }
    ).populate('createdBy', 'name email');

    if (!circular) {
      return res.status(404).json({ message: 'Circular letter not found' });
    }

    res.json(circular);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Delete circular letter
// @route   DELETE /api/circulars/:id
// @access  Private/Admin
exports.deleteCircular = async (req, res) => {
  try {
    const circular = await CircularLetter.findByIdAndDelete(req.params.id);

    if (!circular) {
      return res.status(404).json({ message: 'Circular letter not found' });
    }

    res.json({ message: 'Circular letter removed' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
