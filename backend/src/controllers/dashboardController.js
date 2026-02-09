const Employee = require('../models/Employee');
const Attendance = require('../models/Attendance');
const Document = require('../models/Document');

// @desc    Get dashboard summary
// @route   GET /api/dashboard/summary
// @access  Private
exports.getSummary = async (req, res) => {
  try {
    const currentDate = new Date();
    const lastMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1);
    const currentMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);

    // Total employees
    const totalEmployees = await Employee.countDocuments();
    const lastMonthEmployees = await Employee.countDocuments({
      createdAt: { $lt: currentMonth }
    });
    const employeeChange = lastMonthEmployees > 0 
      ? ((totalEmployees - lastMonthEmployees) / lastMonthEmployees * 100).toFixed(2)
      : 0;

    // Employee absences (current month)
    const totalAbsences = await Attendance.countDocuments({
      date: { $gte: currentMonth }
    });
    const lastMonthAbsences = await Attendance.countDocuments({
      date: { $gte: lastMonth, $lt: currentMonth }
    });
    const absenceChange = lastMonthAbsences > 0
      ? ((totalAbsences - lastMonthAbsences) / lastMonthAbsences * 100).toFixed(2)
      : 0;

    // Total documents
    const totalDocuments = await Document.countDocuments();
    const lastMonthDocuments = await Document.countDocuments({
      createdAt: { $lt: currentMonth }
    });
    const documentChange = lastMonthDocuments > 0
      ? ((totalDocuments - lastMonthDocuments) / lastMonthDocuments * 100).toFixed(2)
      : 0;

    // Total circulars
    const CircularLetter = require('../models/CircularLetter');
    const totalCirculars = await CircularLetter.countDocuments();
    const lastMonthCirculars = await CircularLetter.countDocuments({
      createdAt: { $lt: currentMonth }
    });
    const circularChange = lastMonthCirculars > 0
      ? ((totalCirculars - lastMonthCirculars) / lastMonthCirculars * 100).toFixed(2)
      : 0;

    res.json({
      totalEmployees: {
        count: totalEmployees,
        change: parseFloat(employeeChange)
      },
      employeeAbsence: {
        count: totalAbsences,
        change: parseFloat(absenceChange)
      },
      totalDocuments: {
        count: totalDocuments,
        change: parseFloat(documentChange)
      },
      totalCirculars: {
        count: totalCirculars,
        change: parseFloat(circularChange)
      }
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get attendance summary for chart
// @route   GET /api/dashboard/attendance-summary
// @access  Private
exports.getAttendanceSummary = async (req, res) => {
  try {
    const currentYear = new Date().getFullYear();
    const monthlyData = [];

    for (let month = 0; month < 12; month++) {
      const startDate = new Date(currentYear, month, 1);
      const endDate = new Date(currentYear, month + 1, 0);

      const present = await Attendance.countDocuments({
        date: { $gte: startDate, $lte: endDate }
      });

      const totalEmployees = await Employee.countDocuments();
      const absent = totalEmployees - present;

      monthlyData.push({
        month: new Date(currentYear, month).toLocaleString('en', { month: 'short' }),
        present,
        absent: absent > 0 ? absent : 0
      });
    }

    res.json(monthlyData);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get document submission breakdown
// @route   GET /api/dashboard/document-submission
// @access  Private
exports.getDocumentSubmission = async (req, res) => {
  try {
    const statuses = [
      'awaiting_validation',
      'awaiting_verification',
      'closed',
      'completed',
      'awaiting_signature'
    ];

    const breakdown = [];
    let total = 0;

    for (const status of statuses) {
      const count = await Document.countDocuments({ status });
      total += count;
      breakdown.push({
        status,
        count
      });
    }

    const result = breakdown.map(item => ({
      status: item.status,
      count: item.count,
      percentage: total > 0 ? ((item.count / total) * 100).toFixed(0) : 0
    }));

    res.json({
      total,
      breakdown: result
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
