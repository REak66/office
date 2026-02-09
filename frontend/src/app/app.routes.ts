import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { LoginComponent } from './modules/auth/login/login.component';
import { MainLayoutComponent } from './layouts/main-layout/main-layout.component';
import { DashboardComponent } from './modules/dashboard/dashboard.component';
import { EmployeesComponent } from './modules/employees/employees.component';
import { AttendanceComponent } from './modules/attendance/attendance.component';
import { DocumentsComponent } from './modules/documents/documents.component';
import { CircularComponent } from './modules/circular/circular.component';
import { BannersComponent } from './modules/banners/banners.component';
import { EventsComponent } from './modules/events/events.component';
import { NewsComponent } from './modules/news/news.component';
import { FileMgmtComponent } from './modules/file-mgmt/file-mgmt.component';
import { AdminComponent } from './modules/admin/admin.component';
import { SettingsComponent } from './modules/settings/settings.component';
import { HelpComponent } from './modules/help/help.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  {
    path: '',
    component: MainLayoutComponent,
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: DashboardComponent },
      { path: 'employees', component: EmployeesComponent },
      { path: 'attendance', component: AttendanceComponent },
      { path: 'documents', component: DocumentsComponent },
      { path: 'circular', component: CircularComponent },
      { path: 'banners', component: BannersComponent },
      { path: 'events', component: EventsComponent },
      { path: 'news', component: NewsComponent },
      { path: 'file-mgmt', component: FileMgmtComponent },
      { path: 'admin', component: AdminComponent },
      { path: 'settings', component: SettingsComponent },
      { path: 'help', component: HelpComponent }
    ]
  },
  { path: '**', redirectTo: 'login' }
];
