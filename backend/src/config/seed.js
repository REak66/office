require('dotenv').config();
const mongoose = require('mongoose');
const User = require('../models/User');
const Employee = require('../models/Employee');
const Attendance = require('../models/Attendance');
const Document = require('../models/Document');
const CircularLetter = require('../models/CircularLetter');
const Banner = require('../models/Banner');
const Event = require('../models/Event');
const News = require('../models/News');

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true
    });
    console.log('MongoDB Connected');
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
};

const seedData = async () => {
  try {
    // Clear existing data
    await User.deleteMany({});
    await Employee.deleteMany({});
    await Attendance.deleteMany({});
    await Document.deleteMany({});
    await CircularLetter.deleteMany({});
    await Banner.deleteMany({});
    await Event.deleteMany({});
    await News.deleteMany({});

    console.log('Data cleared');

    // Create Users
    const superAdmin = await User.create({
      name: 'Super Admin Instansi',
      email: 'superadmin@egovern.com',
      password: 'password123',
      role: 'super_admin',
      avatar: 'https://i.pravatar.cc/150?img=1'
    });

    const admin = await User.create({
      name: 'Admin User',
      email: 'admin@egovern.com',
      password: 'password123',
      role: 'admin',
      avatar: 'https://i.pravatar.cc/150?img=2'
    });

    const employeeUsers = [];
    for (let i = 1; i <= 250; i++) {
      const user = await User.create({
        name: `Employee ${i}`,
        email: `employee${i}@egovern.com`,
        password: 'password123',
        role: 'employee',
        avatar: `https://i.pravatar.cc/150?img=${(i % 70) + 1}`
      });
      employeeUsers.push(user);
    }

    console.log('Users created');

    // Create Employees
    const departments = ['IT', 'HR', 'Finance', 'Operations', 'Marketing', 'Sales'];
    const positions = ['Manager', 'Senior', 'Junior', 'Lead', 'Associate'];
    
    const employees = [];
    for (let i = 0; i < employeeUsers.length; i++) {
      const employee = await Employee.create({
        name: employeeUsers[i].name,
        email: employeeUsers[i].email,
        position: positions[i % positions.length],
        department: departments[i % departments.length],
        phone: `+1-555-${String(i).padStart(4, '0')}`,
        address: `${i + 1} Main Street, City`,
        avatar: employeeUsers[i].avatar,
        userId: employeeUsers[i]._id
      });
      employees.push(employee);
    }

    console.log('Employees created');

    // Create Attendance Records
    const currentYear = new Date().getFullYear();
    const attendanceRecords = [];
    
    for (let month = 0; month < 12; month++) {
      const daysInMonth = new Date(currentYear, month + 1, 0).getDate();
      
      for (let day = 1; day <= daysInMonth; day++) {
        // Random 70-80% of employees present each day
        const presentCount = Math.floor(employees.length * (0.7 + Math.random() * 0.1));
        const shuffled = [...employees].sort(() => 0.5 - Math.random());
        const presentEmployees = shuffled.slice(0, presentCount);
        
        for (const emp of presentEmployees) {
          const date = new Date(currentYear, month, day);
          const clockIn = `${8 + Math.floor(Math.random() * 2)}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`;
          const clockOut = `${17 + Math.floor(Math.random() * 2)}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`;
          
          attendanceRecords.push({
            employeeId: emp._id,
            date,
            clockIn,
            clockOut,
            location: Math.random() > 0.5 ? 'Main Office' : 'Branch Office',
            workDuration: '8h 30m',
            type: Math.random() > 0.3 ? 'WFO' : 'WFH'
          });
        }
      }
    }
    
    await Attendance.insertMany(attendanceRecords);
    console.log('Attendance records created');

    // Create Documents
    const documentStatuses = ['awaiting_validation', 'awaiting_verification', 'closed', 'completed', 'awaiting_signature'];
    const documents = [];
    
    for (let i = 0; i < 40; i++) {
      documents.push({
        title: `Document ${i + 1}`,
        description: `Description for document ${i + 1}`,
        submittedBy: employeeUsers[i % employeeUsers.length]._id,
        status: documentStatuses[i % documentStatuses.length],
        category: 'General'
      });
    }
    
    await Document.insertMany(documents);
    console.log('Documents created');

    // Create Circular Letters
    const priorities = ['very_urgent', 'urgent', 'normal'];
    const circulars = [];
    
    for (let i = 0; i < 45; i++) {
      circulars.push({
        title: `Circular Letter ${i + 1}`,
        referenceNumber: `CL-2024-${String(i + 1).padStart(4, '0')}`,
        priority: priorities[i % priorities.length],
        content: `Content of circular letter ${i + 1}`,
        date: new Date(2024, Math.floor(Math.random() * 12), Math.floor(Math.random() * 28) + 1),
        createdBy: admin._id
      });
    }
    
    await CircularLetter.insertMany(circulars);
    console.log('Circular letters created');

    // Create Banners
    const banners = [
      {
        title: 'Welcome to EGOVERN',
        description: 'Your comprehensive officer management system',
        imageUrl: 'https://via.placeholder.com/800x300/4F46E5/ffffff?text=Welcome+Banner',
        isActive: true
      },
      {
        title: 'System Update',
        description: 'New features available now',
        imageUrl: 'https://via.placeholder.com/800x300/10B981/ffffff?text=Update+Banner',
        isActive: true
      }
    ];
    
    await Banner.insertMany(banners);
    console.log('Banners created');

    // Create Events
    const events = [
      {
        title: 'Annual Meeting 2024',
        description: 'Company-wide annual meeting',
        date: new Date(2024, 11, 15),
        location: 'Main Conference Room',
        createdBy: admin._id
      },
      {
        title: 'Training Workshop',
        description: 'Professional development workshop',
        date: new Date(2024, 10, 20),
        location: 'Training Center',
        createdBy: admin._id
      }
    ];
    
    await Event.insertMany(events);
    console.log('Events created');

    // Create News
    const news = [
      {
        title: 'New Office Opening',
        content: 'We are excited to announce the opening of our new branch office.',
        author: admin._id,
        publishedDate: new Date()
      },
      {
        title: 'Employee of the Month',
        content: 'Congratulations to our employee of the month!',
        author: admin._id,
        publishedDate: new Date()
      }
    ];
    
    await News.insertMany(news);
    console.log('News articles created');

    console.log('Seed data created successfully!');
    console.log('\nDefault Login Credentials:');
    console.log('Super Admin:');
    console.log('  Email: superadmin@egovern.com');
    console.log('  Password: password123');
    console.log('\nAdmin:');
    console.log('  Email: admin@egovern.com');
    console.log('  Password: password123');
    console.log('\nEmployee:');
    console.log('  Email: employee1@egovern.com');
    console.log('  Password: password123');

    process.exit(0);
  } catch (error) {
    console.error('Error seeding data:', error);
    process.exit(1);
  }
};

connectDB().then(() => seedData());
