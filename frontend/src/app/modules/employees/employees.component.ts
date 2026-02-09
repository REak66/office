import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { EmployeeService } from '../../core/services/employee.service';
import { Employee } from '../../shared/models/models';

@Component({
  selector: 'app-employees',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './employees.component.html',
  styleUrl: './employees.component.scss'
})
export class EmployeesComponent implements OnInit {
  employees: Employee[] = [];
  showForm = false;
  employeeForm: FormGroup;
  editingId: string | null = null;

  constructor(
    private fb: FormBuilder,
    private employeeService: EmployeeService
  ) {
    this.employeeForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      position: ['', Validators.required],
      department: ['', Validators.required],
      phone: [''],
      address: ['']
    });
  }

  ngOnInit(): void {
    this.loadEmployees();
  }

  loadEmployees(): void {
    this.employeeService.getAll().subscribe({
      next: (data) => this.employees = data,
      error: (err) => console.error('Error loading employees:', err)
    });
  }

  openForm(): void {
    this.showForm = true;
    this.editingId = null;
    this.employeeForm.reset();
  }

  editEmployee(employee: Employee): void {
    this.showForm = true;
    this.editingId = employee._id;
    this.employeeForm.patchValue(employee);
  }

  deleteEmployee(id: string): void {
    if (confirm('Are you sure you want to delete this employee?')) {
      this.employeeService.delete(id).subscribe({
        next: () => this.loadEmployees(),
        error: (err) => console.error('Error deleting employee:', err)
      });
    }
  }

  onSubmit(): void {
    if (this.employeeForm.valid) {
      const data = this.employeeForm.value;
      const request = this.editingId
        ? this.employeeService.update(this.editingId, data)
        : this.employeeService.create(data);

      request.subscribe({
        next: () => {
          this.loadEmployees();
          this.showForm = false;
        },
        error: (err) => console.error('Error saving employee:', err)
      });
    }
  }

  cancel(): void {
    this.showForm = false;
    this.employeeForm.reset();
  }
}
