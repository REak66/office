const User = require('../models/User');

// @desc    Get all admin users
// @route   GET /api/admin
// @access  Private/Admin
exports.getAdmins = async (req, res) => {
  try {
    const admins = await User.find({ 
      role: { $in: ['admin', 'super_admin'] } 
    }).select('-password');
    res.json(admins);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Create admin user
// @route   POST /api/admin
// @access  Private/SuperAdmin
exports.createAdmin = async (req, res) => {
  try {
    const { name, email, password, role } = req.body;

    const userExists = await User.findOne({ email });
    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    const user = await User.create({
      name,
      email,
      password,
      role: role || 'admin'
    });

    const userResponse = user.toObject();
    delete userResponse.password;

    res.status(201).json(userResponse);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Update admin user
// @route   PUT /api/admin/:id
// @access  Private/SuperAdmin
exports.updateAdmin = async (req, res) => {
  try {
    const { password, ...updateData } = req.body;

    const user = await User.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    Object.assign(user, updateData);
    
    if (password) {
      user.password = password;
    }

    await user.save();

    const userResponse = user.toObject();
    delete userResponse.password;

    res.json(userResponse);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Delete admin user
// @route   DELETE /api/admin/:id
// @access  Private/SuperAdmin
exports.deleteAdmin = async (req, res) => {
  try {
    const user = await User.findByIdAndDelete(req.params.id);
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }
    res.json({ message: 'Admin user removed' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
