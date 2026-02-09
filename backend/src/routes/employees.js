const express = require('express');
const router = express.Router();
const {
  getEmployees,
  getEmployeeById,
  createEmployee,
  updateEmployee,
  deleteEmployee
} = require('../controllers/employeeController');
const { auth, adminAuth } = require('../middleware/auth');

router.get('/', auth, getEmployees);
router.get('/:id', auth, getEmployeeById);
router.post('/', auth, adminAuth, createEmployee);
router.put('/:id', auth, adminAuth, updateEmployee);
router.delete('/:id', auth, adminAuth, deleteEmployee);

module.exports = router;
