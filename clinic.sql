-- Question 1
-- Create database
CREATE DATABASE clinicdb;
USE clinicdb;

-- Create Specialties table
CREATE TABLE Specialties (
    specialty_id INT AUTO_INCREMENT PRIMARY KEY,
    specialty_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Doctors table
CREATE TABLE Doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    specialty_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    license_number VARCHAR(50) NOT NULL UNIQUE,
    years_experience INT,
    consultation_fee DECIMAL(10, 2) NOT NULL,
    available_from TIME,
    available_to TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (specialty_id) REFERENCES Specialties(specialty_id) ON DELETE RESTRICT
);

-- Create Patients table
CREATE TABLE Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20) NOT NULL,
    address TEXT,
    blood_group ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
    allergies TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Appointments table
CREATE TABLE Appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    reason_for_visit TEXT NOT NULL,
    status ENUM('Scheduled', 'Completed', 'Cancelled', 'No-show') DEFAULT 'Scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE RESTRICT,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id) ON DELETE RESTRICT,
    -- Ensure a doctor doesn't have multiple appointments at the same time
    UNIQUE KEY (doctor_id, appointment_date, appointment_time)
);

-- Create Payments table
CREATE TABLE Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATETIME NOT NULL,
    payment_method ENUM('Cash', 'Credit Card', 'Debit Card', 'Bank Transfer', 'Mobile Money') NOT NULL,
    payment_status ENUM('Pending', 'Completed', 'Failed', 'Refunded') DEFAULT 'Pending',
    transaction_reference VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id) ON DELETE RESTRICT
);

-- Insert sample data for Specialties
INSERT INTO Specialties (specialty_id, specialty_name, description) VALUES
(1, 'Cardiology', 'Diagnosis and treatment of heart disorders'),
(2, 'Pediatrics', 'Medical care for infants, children, and adolescents'),
(3, 'Orthopedics', 'Treatment of the musculoskeletal system'),
(4, 'Gynecology', 'Women reproductive health'),
(5, 'Neurology', 'Diagnosis and treatment of disorders of the nervous system');

-- Insert sample data for Doctors 
INSERT INTO Doctors (doctor_id, specialty_id, first_name, last_name, email, phone, license_number, years_experience, consultation_fee, available_from, available_to) VALUES
(1, 1, 'Adebayo', 'Owolabi', 'adebayowo@clinic.ng', '08012345678', 'MDCN/2005/45678', 20, 15000.00, '08:00:00', '16:00:00'),
(2, 2, 'Aisha', 'Haruna', 'aishaaruna@clinic.ng', '08023456789', 'MDCN/2010/56789', 15, 12000.00, '09:00:00', '17:00:00'),
(3, 3, 'Chinedu', 'Okeke', 'chinedueke@clinic.ng', '08034567890', 'MDCN/2008/34567', 17, 18000.00, '08:00:00', '15:00:00'),
(4, 4, 'Folake', 'Olu', 'folakeolu@clinic.ng', '08045678901', 'MDCN/2015/67890', 8, 13000.00, '10:00:00', '18:00:00'),
(5, 5, 'Emeka', 'Okafor', 'emeka.okafor@clinic.ng', '08056789012', 'MDCN/2011/78901', 12, 16000.00, '09:00:00', '16:00:00');

-- Insert sample data for Patients 
INSERT INTO Patients (patient_id, first_name, last_name, date_of_birth, gender, email, phone, address, blood_group, allergies) VALUES
(1, 'Chioma', 'Onyekachi', '1985-05-15', 'Female', 'chiomaonyekachi@hotmail.com', '07012345678', '23 Awolowo Road, Lagos', 'O+', 'Penicillin'),
(2, 'Tunde', 'Bakare', '1990-08-22', 'Male', 'tundebakare@gmail.com', '07023456789', '45 Herbert Macaulay Way, Lagos', 'A+', NULL),
(3, 'Aisha', 'Mohammed', '1978-11-10', 'Female', 'aishamohammed@gmail.com', '07034567890', '12 Ibrahim Taiwo Road, Lagos', 'B-', 'Amoxicillin'),
(4, 'Obinna', 'Nwosu', '1982-03-27', 'Male', 'obinnanwosu@yahoo.com', '07045678901', '34 Okpara Avenue, Lagod', 'AB+', 'Latex'),
(5, 'Fatima', 'Obi', '1995-07-03', 'Female', 'fatimaobi@gmail.com', '07056789012', '56 Zoo Road, Lagos', 'O-', NULL);

-- Insert sample data for Appointments 
INSERT INTO Appointments (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason_for_visit, status, notes) VALUES
(1, 1, 4, '2025-05-10', '10:30:00', 'Routine gynecological checkup', 'Scheduled', NULL),
(2, 2, 1, '2025-05-11', '09:15:00', 'Chest pain and shortness of breath', 'Scheduled', 'Patient reported symptoms started last week'),
(3, 3, 5, '2025-05-12', '11:00:00', 'Recurring migraines', 'Scheduled', NULL),
(4, 4, 3, '2025-05-10', '14:00:00', 'Knee pain evaluation', 'Scheduled', 'Patient is a former footballer'),
(5, 5, 2, '2025-05-13', '10:00:00', 'Child wellness checkup', 'Scheduled', NULL);

-- Insert sample data for Payments 
INSERT INTO Payments (payment_id, appointment_id, amount, payment_date, payment_method, payment_status, transaction_reference) VALUES
(1, 1, 13000.00, '2025-05-08 14:25:33', 'Bank Transfer', 'Completed', 'TRF-2025050812345'),
(2, 2, 15000.00, '2025-05-09 10:12:45', 'Credit Card', 'Completed', 'CC-2025050923456'),
(3, 3, 16000.00, '2025-05-10 09:30:22', 'Mobile Money', 'Completed', 'MM-2025051034567'),
(4, 4, 18000.00, '2025-05-08 16:45:17', 'Cash', 'Completed', 'CSH-2025050845678'),
(5, 5, 12000.00, '2025-05-11 11:20:39', 'Debit Card', 'Completed', 'DC-2025051156789');


-- Index for better performance
CREATE INDEX idx_appointments_date ON Appointments(appointment_date);
CREATE INDEX idx_doctor_specialty ON Doctors(specialty_id);
CREATE INDEX idx_patient_name ON Patients(last_name, first_name);
CREATE INDEX idx_payment_status ON Payments(payment_status);




