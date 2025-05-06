from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date
import uvicorn
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Contact Book API", description="A simple CRUD API for a contact book")

# Database connection parameters
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "contactbook")
}

# Create connection pool
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

# Data models
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birthday: Optional[date] = None
    group_id: Optional[int] = None

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    contact_id: int
    created_at: str
    updated_at: str
    
    class Config:
        orm_mode = True

class ContactGroupBase(BaseModel):
    group_name: str
    description: Optional[str] = None

class ContactGroupCreate(ContactGroupBase):
    pass

class ContactGroup(ContactGroupBase):
    group_id: int
    created_at: str
    updated_at: str
    
    class Config:
        orm_mode = True

# API endpoints

# Contact endpoints
@app.post("/contacts/", response_model=Contact, tags=["Contacts"])
def create_contact(contact: ContactCreate, conn=Depends(get_db_connection)):
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Verify group_id exists if provided
        if contact.group_id:
            cursor.execute("SELECT group_id FROM ContactGroups WHERE group_id = %s", (contact.group_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Group not found")
        
        # Check if email already exists
        if contact.email:
            cursor.execute("SELECT contact_id FROM Contacts WHERE email = %s", (contact.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Email already registered")
        
        # Insert new contact
        query = """
        INSERT INTO Contacts (group_id, first_name, last_name, email, phone, address, birthday)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            contact.group_id, 
            contact.first_name, 
            contact.last_name, 
            contact.email, 
            contact.phone, 
            contact.address, 
            contact.birthday
        )
        
        cursor.execute(query, values)
        conn.commit()
        
        # Get the created contact
        contact_id = cursor.lastrowid
        cursor.execute("SELECT * FROM Contacts WHERE contact_id = %s", (contact_id,))
        new_contact = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return new_contact
        
    except Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/contacts/", response_model=List[Contact], tags=["Contacts"])
def read_contacts(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    group_id: Optional[int] = None,
    conn=Depends(get_db_connection)
):
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Base query
        query = "SELECT * FROM Contacts WHERE 1=1"
        params = []
        
        # Add search filter if provided
        if search:
            query += " AND (first_name LIKE %s OR last_name LIKE %s OR email LIKE %s)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term, search_term])
        
        # Add group filter if provided
        if group_id:
            query += " AND group_id = %s"
            params.append(group_id)
        
        # Add pagination
        query += " ORDER BY last_name, first_name LIMIT %s OFFSET %s"
        params.extend([limit, skip])
        
        cursor.execute(query, params)
        contacts = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return contacts
        
    except Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/contacts/{contact_id}", response_model=Contact, tags=["Contacts"])
def read_contact(contact_id: int, conn=Depends(get_db_connection)):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Contacts WHERE contact_id = %s", (contact_id,))
        contact = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
            
        return contact
        
    except Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/contacts/{contact_id}", response_model=Contact, tags=["Contacts"])
def update_contact(contact_id: int, contact: ContactBase, conn=Depends(get_db_connection)):
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Verify contact exists
        cursor.execute("SELECT contact_id FROM Contacts WHERE contact_id = %s", (contact_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Contact not found")
        
        # Verify group_id exists if provided
        if contact.group_id:
            cursor.execute("SELECT group_id FROM ContactGroups WHERE group_id = %s", (contact.group_id,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                raise HTTPException(status_code=404, detail="Group not found")
        
        # Check if email already exists for another contact
        if contact.email:
            cursor.execute("SELECT contact_id FROM Contacts WHERE email = %s AND contact_id != %s", 
                          (contact.email, contact_id))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                raise HTTPException(status_code=400, detail="Email already registered to another contact")
        
        # Update contact
        query = """
        UPDATE Contacts 
        SET group_id = %s, first_name = %s, last_name = %s, email = %s, 
            phone = %s, address = %s, birthday = %s
        WHERE contact_id = %s
        """
        values = (
            contact.group_id, 
            contact.first_name, 
            contact.last_name, 
            contact.email, 
            contact.phone, 
            contact.address, 
            contact.birthday,
            contact_id
        )
        
        cursor.execute(query, values)
        conn.commit()
        
        # Get the updated contact
        cursor.execute("SELECT * FROM Contacts WHERE contact_id = %s", (contact_id,))
        updated_contact = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return updated_contact
        
    except Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/contacts/{contact_id}", tags=["Contacts"])
def delete_contact(contact_id: int, conn=Depends(get_db_connection)):
    try:
        cursor = conn.cursor()
        
        # Verify contact exists
        cursor.execute("SELECT contact_id FROM Contacts WHERE contact_id = %s", (contact_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Contact not found")
        
        # Delete contact
        cursor.execute("DELETE FROM Contacts WHERE contact_id = %s", (contact_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {"message": f"Contact {contact_id} deleted successfully"}
        
    except Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Contact Group endpoints
@app.post("/groups/", response_model=ContactGroup, tags=["Groups"])
def create_group(group: ContactGroupCreate, conn=Depends(get_db_connection)):
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check if group name already exists
        cursor.execute("SELECT group_id FROM ContactGroups WHERE group_name = %s", (group.group_name,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Group name already exists")
        
        # Insert new group
        query = """
        INSERT INTO ContactGroups (group_name, description)
        VALUES (%s, %s)
        """
        values = (group.group_name, group.description)
        
        cursor.execute(query, values)
        conn.commit()
        
        # Get the created group
        group_id = cursor.lastrowid
        cursor.execute("SELECT * FROM ContactGroups WHERE group_id = %s", (group_id,))
        new_group = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return new_group
        
    except Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/groups/", response_model=List[ContactGroup], tags=["Groups"])
def read_groups(conn=Depends(get_db_connection)):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ContactGroups ORDER BY group_name")
        groups = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return groups
        
    except Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/groups/{group_id}", response_model=ContactGroup, tags=["Groups"])
def read_group(group_id: int, conn=Depends(get_db_connection)):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ContactGroups WHERE group_id = %s", (group_id,))
        group = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
            
        return group
        
    except Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/groups/{group_id}", response_model=ContactGroup, tags=["Groups"])
def update_group(group_id: int, group: ContactGroupBase, conn=Depends(get_db_connection)):
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Verify group exists
        cursor.execute("SELECT group_id FROM ContactGroups WHERE group_id = %s", (group_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Group not found")
        
        # Check if group name already exists for another group
        cursor.execute("SELECT group_id FROM ContactGroups WHERE group_name = %s AND group_id != %s", 
                      (group.group_name, group_id))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Group name already exists")
        
        # Update group
        query = """
        UPDATE ContactGroups 
        SET group_name = %s, description = %s
        WHERE group_id = %s
        """
        values = (group.group_name, group.description, group_id)
        
        cursor.execute(query, values)
        conn.commit()
        
        # Get the updated group
        cursor.execute("SELECT * FROM ContactGroups WHERE group_id = %s", (group_id,))
        updated_group = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return updated_group
        
    except Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/groups/{group_id}", tags=["Groups"])
def delete_group(group_id: int, conn=Depends(get_db_connection)):
    try:
        cursor = conn.cursor()
        
        # Verify group exists
        cursor.execute("SELECT group_id FROM ContactGroups WHERE group_id = %s", (group_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Group not found")
        
        # Check if group has contacts
        cursor.execute("SELECT COUNT(*) FROM Contacts WHERE group_id = %s", (group_id,))
        contact_count = cursor.fetchone()[0]
        
        if contact_count > 0:
            # Set group_id to NULL for contacts in this group
            cursor.execute("UPDATE Contacts SET group_id = NULL WHERE group_id = %s", (group_id,))
        
        # Delete group
        cursor.execute("DELETE FROM ContactGroups WHERE group_id = %s", (group_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {"message": f"Group {group_id} deleted successfully. {contact_count} contacts updated."}
        
    except Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)