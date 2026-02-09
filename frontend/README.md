# Officer Management System - Frontend

Angular 17 frontend application for the Officer Management System.

## Features

- **Authentication**: Login with JWT token authentication
- **Dashboard**: Overview with summary cards and charts
  - Employee statistics
  - Attendance tracking
  - Document management
  - Circular letters overview
- **Employee Management**: CRUD operations for employees
- **Attendance Management**: Track employee attendance (WFO/WFH)
- **Document Management**: Manage organizational documents
- **Circular Letters**: Create and manage circular letters
- **Banner Management**: Manage promotional banners
- **Events**: Create and manage organizational events
- **News**: Publish and manage news articles
- **File Management**: Upload and manage files
- **Admin Panel**: User management and role assignment

## Tech Stack

- Angular 17 (Standalone Components)
- TypeScript
- SCSS
- ng2-charts (Chart.js integration)
- RxJS
- Angular Reactive Forms

## Prerequisites

- Node.js (v18 or higher)
- npm (v9 or higher)

## Installation

```bash
# Install dependencies
npm install --legacy-peer-deps
```

## Development Server

```bash
# Start development server
npm start

# Navigate to http://localhost:4200
```

## Build

```bash
# Build for production
npm run build

# Output will be in dist/ directory
```

## Project Structure

```
src/
├── app/
│   ├── core/
│   │   ├── guards/         # Route guards
│   │   ├── interceptors/   # HTTP interceptors
│   │   └── services/       # API services
│   ├── layouts/           # Layout components
│   │   └── main-layout/
│   ├── modules/           # Feature modules
│   │   ├── admin/
│   │   ├── attendance/
│   │   ├── auth/
│   │   ├── banners/
│   │   ├── circular/
│   │   ├── dashboard/
│   │   ├── documents/
│   │   ├── employees/
│   │   ├── events/
│   │   ├── file-mgmt/
│   │   ├── help/
│   │   ├── news/
│   │   └── settings/
│   ├── shared/
│   │   ├── components/    # Shared components
│   │   │   ├── header/
│   │   │   └── sidebar/
│   │   └── models/        # TypeScript interfaces
│   ├── app.component.ts
│   ├── app.config.ts
│   └── app.routes.ts
├── environments/
├── styles.scss
└── index.html
```

## API Configuration

The API endpoint is configured in `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:5000/api'
};
```

## Available Routes

- `/login` - Login page (public)
- `/dashboard` - Dashboard overview (protected)
- `/employees` - Employee management (protected)
- `/attendance` - Attendance tracking (protected)
- `/documents` - Document management (protected)
- `/circular` - Circular letters (protected)
- `/banners` - Banner management (protected)
- `/events` - Event management (protected)
- `/news` - News management (protected)
- `/file-mgmt` - File management (protected)
- `/admin` - User administration (protected)
- `/settings` - Settings (protected)
- `/help` - Help page (protected)

## Styling

The application uses a clean, modern design with:
- White background with subtle shadows
- Rounded cards and components
- Professional color scheme
- Responsive layout
- Clean typography

## Authentication

The application uses JWT token authentication:
1. User logs in through `/login`
2. Token is stored in localStorage
3. HTTP interceptor adds token to all API requests
4. Auth guard protects routes from unauthorized access

## Charts

The dashboard includes:
- **Line Chart**: Employee Attendance Summary (using Chart.js)
- **Donut Chart**: Document Submission breakdown (using Chart.js)

## Development Notes

- All components use Angular 17 standalone pattern
- Reactive forms for all data input
- Proper error handling throughout
- TypeScript strict mode enabled
- SCSS for styling

## License

MIT
