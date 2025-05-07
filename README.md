# MySQL Database & FastAPI Development Project - Clinic Database & Contact Book API

> **⚠️Security Note**: This project includes configuration files for database connections. Never commit real credentials to GitHub. Use the provided example files and create your own `.env` file locally that is not tracked by git.

This repository contains my solutions for two database development assignments: a clinical management system database and a contact book API.

## 📌Project Description

### Question 1: Clinic Management System
A comprehensive SQL database for managing a medical clinic's operations. The database supports tracking of:
- Medical specialties
- Doctors and their specialties
- Patients and their medical information
- Appointments between doctors and patients
- Payments for medical services

### Question 2: Contact Book API
A CRUD API built with FastAPI and MySQL that allows users to:
- Manage contacts (create, view, update, delete)
- Organize contacts into groups
- Search and filter contacts
- Handle data validation and relationships

## 🚀How to Run/Setup

### ✅Setting up Question 1 (Clinic Database)
1. Ensure you have MySQL installed
2. Import the database schema and sample data:
   ```
   mysql -u your_username -p < clinic.sql
   ```

### ✅Setting up Question 2 (Contact Book API)
1. Install Python 3.7+ and required packages:
   ```
   pip install -r requirements.txt
   ```
2. Import the database schema:
   ```
   mysql -u your_username -p < contactbook.sql
   ```
3. Create a `.env` file based on the provided `env.txt` example:
   ```
   # Create a new .env file (do not commit this file to GitHub)
   cp env.txt .env
   # Edit the .env file with your actual database credentials
   ```
4. Start the FastAPI server:
   ```
   python main.py
   ```
5. Access the API at `http://localhost:8000`
6. View interactive API documentation at `http://localhost:8000/docs`

## 🛠️Database ERD (Entity Relationship Diagrams)

### Clinic Management System ERD
![Clinic Management System ERD](https://github.com/Nwamaka77/Database-Week-8-Assignment/blob/main/clinicdbERD.png)

### Contact Book API ERD
![Contact Book API ERD](https://github.com/Nwamaka77/Database-Week-8-Assignment/blob/main/contactbookERD.png)

## 📂Project Files

### Question 1
- `clinic.sql` - Well-commented SQL file containing database creation, table definitions with proper constraints, relationships, indexes, and sample data

### Question 2
- `contactbook.sql` - SQL script to create the contact book database
- `main.py` - FastAPI application with endpoint definitions
- `requirements.txt` - Python dependencies
- `env.txt` - Sample environment variables configuration (do not put real credentials in this file)

## 🔒Security Best Practices

### Environment Variables
- The `env.txt` file is included as an example only
- Create a local `.env` file based on this example with your actual credentials
- Add `.env` to your `.gitignore` file to prevent committing sensitive information
- Never commit actual credentials to your repository




  
