import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

interface MenuItem {
  label: string;
  icon: string;
  route: string;
}

@Component({
    selector: 'app-sidebar',
    imports: [CommonModule, RouterModule],
    templateUrl: './sidebar.component.html',
    styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {
  menuItems: MenuItem[] = [
    { label: 'Dashboard', icon: '📊', route: '/dashboard' },
    { label: 'Banner', icon: '🖼️', route: '/banners' },
    { label: 'Attendance', icon: '📅', route: '/attendance' },
    { label: 'Document', icon: '📄', route: '/documents' },
    { label: 'Circular Letter', icon: '✉️', route: '/circular' },
    { label: 'File Management', icon: '📁', route: '/file-mgmt' },
    { label: 'Event', icon: '🎉', route: '/events' },
    { label: 'News', icon: '📰', route: '/news' },
    { label: 'Manage Employees', icon: '👥', route: '/employees' },
    { label: 'Manage Admin', icon: '👤', route: '/admin' },
    { label: 'Help', icon: '❓', route: '/help' },
    { label: 'Setting', icon: '⚙️', route: '/settings' }
  ];
}
