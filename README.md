# Officer Management System

A complete full-stack web application for managing organizational operations including employees, attendance, documents, circulars, events, news, and more.

## ⚠️ SECURITY NOTICE

**IMPORTANT**: This application uses Angular 17.3.12 which has known XSS vulnerabilities. 

**For Development/Testing**: Safe to use with restrictions (see SECURITY_SUMMARY.md)

**Before Production Deployment**: 
- **MUST upgrade Angular to 19.2.18+** to fix XSS vulnerabilities
- **MUST implement rate limiting** on API endpoints
- See `SECURITY_SUMMARY.md` and `ANGULAR_SECURITY_UPGRADE.md` for details

## Project Structure

```
office/
├── backend/     # Node.js + Express + MongoDB backend
└── frontend/    # Angular 17 frontend
```

## Features

### Backend (Node.js + Express + MongoDB)
- RESTful API with JWT authentication
- User management with role-based access control
- Employee CRUD operations
- Attendance tracking (WFO/WFH)
- Document management
- Circular letter management
- Banner management
- Event management
- News management
- File upload/download
- Dashboard analytics

### Frontend (Angular 17)
- Modern, responsive UI
- Authentication with JWT tokens
- Interactive dashboard with charts
- CRUD interfaces for all modules
- File management
- Real-time data updates
- Role-based access control

## Tech Stack

### Backend
- Node.js & Express.js
- MongoDB with Mongoose
- JWT Authentication
- Multer (File uploads)
- bcrypt (Password hashing)

### Frontend
- Angular 17 (Standalone Components)
- TypeScript
- SCSS
- Chart.js & ng2-charts
- RxJS
- Angular Reactive Forms

## Getting Started

### Prerequisites
- Node.js (v18 or higher)
- MongoDB (v6 or higher)
- npm (v9 or higher)

### Backend Setup

```bash
cd backend
npm install
cp .env.example .env  # Configure your environment variables
npm run dev
```

Backend will run on `http://localhost:5000`

### Frontend Setup

```bash
cd frontend
npm install --legacy-peer-deps
npm start
```

Frontend will run on `http://localhost:4200`

## API Endpoints

See `backend/README.md` for detailed API documentation.

## Seeding Sample Data

To populate the database with sample data (250 employees, attendance records, documents, etc.):

```bash
cd backend
npm run seed
```

## Default Users

After seeding, you can login with:
- **Super Admin**: superadmin@egovern.com / password123
- **Admin**: admin@egovern.com / password123  
- **Employee**: employee1@egovern.com / password123

## License

MIT
