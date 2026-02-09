import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-settings',
    imports: [CommonModule],
    template: `
    <div class="page">
      <h1>Settings</h1>
      <div class="card">
        <p>Settings page - Coming soon</p>
      </div>
    </div>
  `,
    styleUrls: ['../employees/employees.component.scss']
})
export class SettingsComponent {}
