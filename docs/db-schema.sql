-- docs/db-schema.sql
CREATE DATABASE IF NOT EXISTS lavisco_hrms;
USE lavisco_hrms;

CREATE TABLE departments (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  role ENUM('admin', 'hrOfficer', 'employee') NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  phone VARCHAR(20),
  department_id INT,
  is_locked BOOLEAN DEFAULT FALSE,
  failed_login_attempts INT DEFAULT 0,
  locked_until DATETIME NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE leave_requests (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  type VARCHAR(50),
  status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
  days_requested INT AS (DATEDIFF(end_date, start_date) + 1) STORED,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  reviewed_by INT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (reviewed_by) REFERENCES users(id)
);

CREATE TABLE payroll_cycles (
  id INT PRIMARY KEY AUTO_INCREMENT,
  month_year VARCHAR(7) NOT NULL,
  status ENUM('draft', 'pending_approval', 'approved') DEFAULT 'draft',
  created_by INT NOT NULL,
  approved_by INT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  approved_at TIMESTAMP NULL,
  FOREIGN KEY (created_by) REFERENCES users(id),
  FOREIGN KEY (approved_by) REFERENCES users(id)
);

CREATE TABLE payroll_records (
  id INT PRIMARY KEY AUTO_INCREMENT,
  payroll_cycle_id INT NOT NULL,
  user_id INT NOT NULL,
  base_salary DECIMAL(12,2),
  bonus DECIMAL(12,2) DEFAULT 0,
  deductions DECIMAL(12,2) DEFAULT 0,
  net_pay DECIMAL(12,2) AS (base_salary + bonus - deductions) STORED,
  payslip_encrypted BLOB,
  payslip_iv VARBINARY(12),
  payslip_auth_tag VARBINARY(16),
  payslip_ready BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (payroll_cycle_id) REFERENCES payroll_cycles(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE disciplinary_actions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  type ENUM('first_warning', 'final_warning', 'suspension') NOT NULL,
  reason TEXT NOT NULL,
  issued_by INT NOT NULL,
  approved_by INT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (issued_by) REFERENCES users(id),
  FOREIGN KEY (approved_by) REFERENCES users(id)
);

CREATE TABLE documents (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  type ENUM('contract', 'id_copy', 'certificate') NOT NULL,
  file_name VARCHAR(255),
  file_encrypted BLOB,
  file_iv VARBINARY(12),
  file_auth_tag VARBINARY(16),
  expiry_date DATE NULL,
  uploaded_by INT NOT NULL,
  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (uploaded_by) REFERENCES users(id)
);

-- Insert sample data
INSERT INTO departments (name) VALUES ('HR'), ('Engineering'), ('Finance');

-- Admin user: email=admin@lavisco.com, password=admin123
-- bcrypt hash for "admin123"
INSERT INTO users (role, email, password_hash, first_name, last_name, department_id)
VALUES ('admin', 'admin@lavisco.com', '$2b$12$Kix8l5W1r6uRqD5J3e8QfO2xX9UqR7zF2vJ1X3Y4Z5a6b7c8d9e0f', 'System', 'Admin', 1);
