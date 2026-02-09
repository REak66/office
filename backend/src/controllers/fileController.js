const File = require('../models/File');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

// Configure multer for file upload
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const uploadDir = path.join(__dirname, '../../uploads');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const upload = multer({ storage: storage });

// @desc    Upload file
// @route   POST /api/files/upload
// @access  Private
exports.uploadFile = [
  upload.single('file'),
  async (req, res) => {
    try {
      if (!req.file) {
        return res.status(400).json({ message: 'No file uploaded' });
      }

      const file = await File.create({
        fileName: req.file.filename,
        originalName: req.file.originalname,
        path: req.file.path,
        size: req.file.size,
        uploadedBy: req.user._id
      });

      const populatedFile = await File.findById(file._id).populate('uploadedBy', 'name email');
      res.status(201).json(populatedFile);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }
];

// @desc    Get all files
// @route   GET /api/files
// @access  Private
exports.getFiles = async (req, res) => {
  try {
    const files = await File.find()
      .populate('uploadedBy', 'name email')
      .sort({ createdAt: -1 });
    res.json(files);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Download file
// @route   GET /api/files/:id/download
// @access  Private
exports.downloadFile = async (req, res) => {
  try {
    const file = await File.findById(req.params.id);
    if (!file) {
      return res.status(404).json({ message: 'File not found' });
    }

    res.download(file.path, file.originalName);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Delete file
// @route   DELETE /api/files/:id
// @access  Private/Admin
exports.deleteFile = async (req, res) => {
  try {
    const file = await File.findById(req.params.id);
    if (!file) {
      return res.status(404).json({ message: 'File not found' });
    }

    // Delete file from filesystem
    if (fs.existsSync(file.path)) {
      fs.unlinkSync(file.path);
    }

    await File.findByIdAndDelete(req.params.id);
    res.json({ message: 'File removed' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
