import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-help',
    imports: [CommonModule],
    template: `
    <div class="page">
      <h1>Help</h1>
      <div class="card">
        <h2>Officer Management System - Help</h2>
        <p>Welcome to the help section. Here you can find information about using the system.</p>
        <h3>Getting Started</h3>
        <ul>
          <li>Use the sidebar to navigate between different sections</li>
          <li>Click on the + button to add new records</li>
          <li>Use the edit and delete icons to manage existing records</li>
        </ul>
      </div>
    </div>
  `,
    styleUrls: ['../employees/employees.component.scss']
})
export class HelpComponent {}
