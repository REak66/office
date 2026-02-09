const mongoose = require('mongoose');

const circularLetterSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  referenceNumber: {
    type: String,
    required: true
  },
  priority: {
    type: String,
    enum: ['very_urgent', 'urgent', 'normal'],
    default: 'normal'
  },
  content: {
    type: String,
    required: true
  },
  date: {
    type: Date,
    default: Date.now
  },
  createdBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('CircularLetter', circularLetterSchema);
