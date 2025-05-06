-- Question 2
-- Create database
CREATE DATABASE contactbook;
USE contactbook;

-- Create Contact Group table
CREATE TABLE ContactGroups (
    group_id INT AUTO_INCREMENT PRIMARY KEY,
    group_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Contact table
CREATE TABLE Contacts (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    address TEXT,
    birthday DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES ContactGroups(group_id) ON DELETE SET NULL
);

-- Add indexes for better performance
CREATE INDEX idx_contact_name ON Contacts(last_name, first_name);
CREATE INDEX idx_contact_email ON Contacts(email);
CREATE INDEX idx_contact_group ON Contacts(group_id);

-- Insert sample data for ContactGroups
INSERT INTO ContactGroups (group_id, group_name, description) VALUES
(1, 'Family', 'Close family members'),
(2, 'Friends', 'Personal friends'),
(3, 'Work', 'Professional contacts'),
(4, 'School', 'Classmates and teachers');

-- Insert sample data for Contacts
INSERT INTO Contacts (contact_id, group_id, first_name, last_name, email, phone, address, birthday) VALUES
(1, 1, 'Chioma', 'Umeh', 'chiome24@yahoo.com', '08012345678', '123 Main St, Lagos', '1985-06-15'),
(2, 1, 'George', 'Umeh', 'georgy23@gmail.com', '08023456789', '123 Main St, Lagos', '1988-03-22'),
(3, 2, 'Amara', 'Okafor', 'amara.okafor@example.com', '08034567890', '45 Park Avenue, Lagos', '1990-11-10'),
(4, 3, 'Taiwo', 'Adeyemi', 'taiwo.adeyemi@company.com', '08045678901', '67 Business Road, Lagos', '1982-07-27'),
(5, 3, 'Chidi', 'Nwosu', 'chidi.nwosu@company.com', '08056789012', '89 Office Street, Lagos', '1991-01-03'),
(6, 4, 'Ngozi', 'Eze', 'ngozi.eze@school.edu', '08067890123', '12 Campus Drive, Lagos', '1995-09-12');
