const mongoose = require('mongoose');

const attendanceSchema = new mongoose.Schema({
  employeeId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Employee',
    required: true
  },
  date: {
    type: Date,
    required: true
  },
  clockIn: {
    type: String,
    required: true
  },
  clockOut: {
    type: String,
    default: ''
  },
  location: {
    type: String,
    default: ''
  },
  workDuration: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    enum: ['WFO', 'WFH'],
    default: 'WFO'
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Attendance', attendanceSchema);
