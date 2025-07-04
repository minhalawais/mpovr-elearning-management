# Standard library imports
import os
import string
import random
import re
import json
import csv
import io
import calendar
import threading
import time
from datetime import datetime, timedelta
from collections import defaultdict

# Third-party library imports
import mysql.connector
from mysql.connector import pooling
from mysql.connector.errors import PoolError, DatabaseError

import pandas as pd
import numpy as np

import requests

from PIL import Image, ImageDraw, ImageFont
import qrcode

import pytz


from flask import Response
from werkzeug.utils import secure_filename

# Local imports
from sms_service import send_login_password_email,send_bounced_complaint_email,send_rca_capa_reminder_email
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
from matplotlib.patches import Rectangle
import matplotlib.patheffects as path_effects
from bidi.algorithm import get_display
import arabic_reshaper
from matplotlib.patches import Patch
import matplotlib.font_manager as fm
from typing import Optional, Dict, Union,List
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = "AIzaSyDYg5itguljMb-ado1Q4LOxZLPihp0DJ5A"

# Configure the API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
# Database configuration
dbconfigs = {
    "admin": {
        "host": "localhost",
        "user": "user-for-admin",
        "password": "M.m03007493358",
        "database": "fos-database"
    },
    "complaints": {
        "host": "localhost",
        "user": "user-for-complaints",
        "password": "M.m03007493358",
        "database": "fos-database"
    },
    "io": {
        "host": "localhost",
        "user": "user-for-io",
        "password": "M.m03007493358",
        "database": "fos-database"
    },
    "personal": {
        "host": "localhost",
        "user": "fos-database",
        "password": "M.m03007493358",
        "database": "fos-database"
    },
    "user-admin1": {
        "host": "localhost",
        "user": "user-admin1",
        "password": "M.m03007493358",
        "database": "fos-database"
    },
    "user-admin2": {
        "host": "localhost",
        "user": "user-admin2",
        "password": "M.m03007493358",
        "database": "fos-database"
    },
    "user-admin3": {
        "host": "localhost",
        "user": "user-admin3",
        "password": "M.m03007493358",
        "database": "fos-database"
    },
    "user-admin4": {
        "host": "localhost",
        "user": "user-admin4",
        "password": "M.m03007493358",
        "database": "fos-database"
    },
    "user-admin5": {
        "host": "localhost",
        "user": "user-admin5",
        "password": "M.m03007493358",
        "database": "fos-database"
    }
}



pakistani_tz = pytz.timezone('Asia/Karachi')

# Initialize pools dictionary
pools = {}
validJudges = [
  "AbdulRehman", "SarimMehmood", "MiqdamJunaid", "SamanAslam", 
  "SarahBlanchard", "KarlBorgschulze", "RittaShine", "SagarMehmood", 
  "BariraHanif", "HaziqAhmed", "SamanHaseeb", "BadarUzaman", 
  "NaeemQureshi", "ShahbazSharif","JustajuVentures"
];

MAX_RETRIES = 10
BASE_DELAY = 1  # time in seconds
MAX_DELAY = 30  # maximum delay in seconds

def get_retryable_connection(purpose):
    temp_users = ['user-admin1', 'user-admin2', 'user-admin3', 'user-admin4', 'user-admin5']
    all_users = [purpose] + temp_users
    
    for attempt in range(MAX_RETRIES):
        random.shuffle(all_users)  # Randomize user order to distribute load
        for user in all_users:
            try:
                pool = get_pool(user)
                start_time = time.time()
                while time.time() - start_time < 5:  # 5-second timeout
                    try:
                        connection = pool.get_connection()
                        if connection.is_connected():
                            return connection
                        else:
                            connection.close()
                            raise mysql.connector.InterfaceError("Invalid connection")
                    except mysql.connector.PoolError:
                        time.sleep(0.1)  # Short sleep before retrying
                raise mysql.connector.PoolError("Connection attempt timed out")
            except (mysql.connector.PoolError, mysql.connector.InterfaceError) as e:
                if "max_user_connections" in str(e) or "pool exhausted" in str(e):
                    print(f"Connection issue for {user}: {str(e)}. Trying next user.")
                    continue
                else:
                    raise
        
        # If we've tried all users and still haven't connected, wait and retry
        delay = min(BASE_DELAY * (2 ** attempt) + random.uniform(0, 1), MAX_DELAY)
        print(f"All users at connection limit. Retrying in {delay:.2f} seconds...")
        time.sleep(delay)
    
    raise mysql.connector.OperationalError("Failed to establish a database connection after maximum retries")

def get_pool(purpose):
    if purpose not in pools:
        config = dbconfigs[purpose]
        pools[purpose] = pooling.MySQLConnectionPool(
            pool_name=f"{purpose}_pool",
            pool_size=10,  # Reduced pool size
            pool_reset_session=True,
            **config
        )
    return pools[purpose]

def close_all_connections():
    for pool in pools.values():
        pool.close()
def update_mobile_number(mobile):
    mobile = re.sub(r'\D', '', mobile)
    
    if mobile.startswith('03'):
        return '923' + mobile[2:]
    elif mobile.startswith('3'):
        return '923' + mobile[1:]
    else:
        return mobile


def get_db_connection():
    """
    Establish and return a MySQL database connection.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='nutribiz',
            password='M.m03007493358',
            database='nutribiz'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def check_judge_grading_status(judge_name: str, participant_name: str) -> bool:
    """
    Check if a judge has already graded a specific participant.
    
    Args:
        judge_name (str): Name of the judge
        participant_name (str): Name of the participant
    
    Returns:
        bool: True if judge has already graded, False otherwise
    """
    connection = get_db_connection()
    if not connection:
        return True  # Assume already graded to prevent duplicate submission
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM judge_response WHERE judge_name = %s AND participant_name = %s"
        cursor.execute(query, (judge_name, participant_name))
        results = cursor.fetchall()
        
        return len(results) > 0
    except mysql.connector.Error as err:
        print(f"Error checking grading status: {err}")
        return True
    finally:
        if connection:
            cursor.close()
            connection.close()

def save_judge_responses(
    judge_name: str, 
    participant_name: str, 
    responses: List[Union[str, int, float]]
) -> bool:
    """
    Save judge's responses to the database.
    
    Args:
        judge_name (str): Name of the judge
        participant_name (str): Name of the participant
        responses (List): List of 5 responses
    
    Returns:
        bool: True if responses saved successfully, False otherwise
    """
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO judge_response 
        (judge_name, participant_name, question1, question2, question3, question4, question5)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = [judge_name, participant_name] + responses
        
        cursor.execute(query, values)
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error saving responses: {err}")
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()
def fetch_judge_responses(judge_name: str) -> Union[List[Dict], None]:
    """
    Fetch all responses for a specific judge from the database.
    
    Args:
        judge_name (str): Name of the judge
    
    Returns:
        Union[List[Dict], None]: List of response dictionaries or None if an error occurs
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        # Use dictionary cursor to return results as dictionaries
        cursor = connection.cursor(dictionary=True)
        
        # Query to fetch all responses for the judge
        query = "SELECT * FROM judge_response WHERE judge_name = %s"
        cursor.execute(query, (judge_name,))
        
        # Fetch all results
        results = cursor.fetchall()
        
        return results
    
    except mysql.connector.Error as err:
        print(f"Error fetching responses: {err}")
        return None
    
    finally:
        # Always close cursor and connection
        if connection:
            cursor.close()
            connection.close()
def check_judge_consent(judge_name: str) -> Optional[bool]:
    """
    Check the consent status for a specific judge.
    
    Args:
        judge_name (str): Name of the judge
    
    Returns:
        Optional[bool]: 
        - False if judge doesn't exist in the database
        - Consent status (True/False) if judge exists
        - None if there's a database error
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        # Use dictionary cursor to return results as dictionaries
        cursor = connection.cursor(dictionary=True)
        
        # Query to fetch consent status for the judge
        query = "SELECT consent_given FROM judge_consents WHERE judge_name = %s"
        cursor.execute(query, (judge_name,))
        
        # Fetch the result
        result = cursor.fetchone()
        
        # If no result, return False (judge doesn't exist)
        if result is None:
            return False
        
        # Return the consent status
        return bool(result['consent_given'])
    
    except mysql.connector.Error as err:
        print(f"Error checking consent status: {err}")
        return None
    
    finally:
        # Always close cursor and connection
        if connection:
            cursor.close()
            connection.close()
            
def check_judge_exists(connection, judge_name: str) -> bool:
    """
    Check if a judge already exists in the consent table.
    
    Args:
        connection (mysql.connector.connection.MySQLConnection): Database connection
        judge_name (str): Name of the judge
    
    Returns:
        bool: True if judge exists, False otherwise
    """
    try:
        cursor = connection.cursor()
        check_query = "SELECT * FROM judge_consents WHERE judge_name = %s"
        cursor.execute(check_query, (judge_name,))
        results = cursor.fetchall()
        return len(results) > 0
    except mysql.connector.Error as err:
        print(f"Error checking judge existence: {err}")
        raise

def update_judge_consent(judge_name: str, consent_given: bool) -> Optional[bool]:
    """
    Update or insert judge's consent status.
    
    Args:
        judge_name (str): Name of the judge
        consent_given (bool): Consent status to be recorded
    
    Returns:
        Optional[bool]: True if successful, None if an error occurred
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        # Start a transaction
        connection.start_transaction()
        
        # Check if judge exists
        judge_exists = check_judge_exists(connection, judge_name)
        
        cursor = connection.cursor()
        
        if not judge_exists:
            # Insert new consent record
            insert_query = """
            INSERT INTO judge_consents (judge_name, consent_given) 
            VALUES (%s, %s)
            """
            cursor.execute(insert_query, (judge_name, consent_given))
        else:
            # Update existing consent record
            update_query = """
            UPDATE judge_consents 
            SET consent_given = %s 
            WHERE judge_name = %s
            """
            cursor.execute(update_query, (consent_given, judge_name))
        
        # Commit the transaction
        connection.commit()
        return True
    
    except mysql.connector.Error as err:
        # Rollback the transaction in case of error
        connection.rollback()
        print(f"Error recording consent: {err}")
        return None
    
    finally:
        # Always close cursor and connection
        if connection:
            cursor.close()
            connection.close()
def update_phone_numbers():
    
    try:
        # Step 1: Load the updated phone numbers from the file into a DataFrame
        updated_phones = pd.read_excel('Sadaqat Updated Data.xlsx')

        # Step 2: Connect to the MySQL database
        connection = get_retryable_connection('personal')
        cursor = connection.cursor()

        # Step 3: Fetch existing employees' data from the database into a DataFrame
        cursor.execute('SELECT company_id, employee_name, mobile_number FROM employees where office_id between 72 and 122 and employee_left = false')
        employees_data = cursor.fetchall()

        employees = pd.DataFrame(employees_data, columns=['company_id', 'employee_name', 'mobile_number'])
        print(employees)
        updated_phones = updated_phones.dropna(subset=['company_id'])

        employees['company_id'] = employees['company_id'].astype(str)
        updated_phones['company_id'] = updated_phones['company_id'].astype(int)
        updated_phones['company_id'] = updated_phones['company_id'].astype(str)
        print(updated_phones)
        # Step 4: Merge the DataFrames to match employees by company_id
        employees['mobile_number'] = employees['mobile_number'].astype(str)
        updated_phones['mobile_number'] = updated_phones['mobile_number'].astype(str)
        employees['mobile_number'] = employees['mobile_number'].apply(update_mobile_number)
        updated_phones['mobile_number'] = updated_phones['mobile_number'].apply(update_mobile_number)

        merged_df = pd.merge(employees, updated_phones, on='company_id', suffixes=('_old', '_new'))
        print(merged_df)
        # Identify the records with updated phone numbers
        updated_records = merged_df[merged_df['mobile_number_old'] != merged_df['mobile_number_new']]
        print(updated_records)
        # Step 5: Update the phone numbers in the MySQL database
        for index, row in updated_records.iterrows():
            update_query = """UPDATE employees SET mobile_number = %s WHERE company_id = %s"""
            cursor.execute(update_query, (row['mobile_number_new'], row['company_id']))
        # Commit the changes
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        print("Phone numbers updated successfully.")
    except Exception as e:
        print("An error occurred:", str(e))
def insert_complaints(database_table_name='complaints'):
    # Read complaints file into a DataFrame
    complaints_df = pd.read_excel('Book3.xlsx')

    db_connection = get_retryable_connection('admin')
    cursor = db_connection.cursor()

    try:
        # Iterate through each complaint
        for index, complaint in complaints_df.iterrows():
            complaint = complaint.where(pd.notna(complaint), None)
            ticket_number = complaint['ticket_number']

            # Convert columns with 'date' in their names to the correct datetime format
            date_columns = [col for col in complaint.index if 'date' in col.lower()]
            complaint[date_columns] = complaint[date_columns].apply(pd.to_datetime, format='%m/%d/%Y %H:%M', errors='coerce')

            # Check if the complaint with the given ticket_number exists in the database
            select_query = f"SELECT * FROM {database_table_name} WHERE ticket_number = %s"
            cursor.execute(select_query, (ticket_number,))
            existing_complaint = cursor.fetchone()

            if existing_complaint is None:
                # Convert the timestamps to strings in the format 'YYYY-MM-DD HH:MM:SS'
                complaint[date_columns] = complaint[date_columns].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notna(x) else None)
                complaint['complaint_no'] = int(complaint['complaint_no']) + 500
                # Insert the complaint into the database
                insert_query = f"INSERT INTO {database_table_name} VALUES ({','.join(['%s'] * len(complaint))})"
                cursor.execute(insert_query, tuple(complaint))
                print(f"Inserted complaint with ticket_number: {ticket_number}")

        # Commit the changes to the database
        db_connection.commit()

    except mysql.connector.Error as err:
        print(f"Error inserting complaints: {ticket_number} {err}")

    finally:
        # Close the database connection
        cursor.close()
        db_connection.close()
    





def generate_leavers_joiners(file):
    try:
        conn = get_retryable_connection('admin')
        query = "SELECT * FROM employees;"

        # Use pandas to read data from MySQL and convert it to a DataFrame
        database_df = pd.read_sql(query, conn)
        database_df['mobile_number'] = database_df['mobile_number'].astype(str)
        database_df['mobile_number'] = database_df['mobile_number'].apply(update_mobile_number)
        database_df['mobile_number'] =  pd.to_numeric(database_df['mobile_number'], errors='coerce').astype('Int64')
        database_df['mobile_number'] = database_df['mobile_number'].astype(str)
        database_df['employee_name'] = database_df['employee_name'].str.lower()
        database_df.loc[~database_df['mobile_number'].astype(str).str.startswith('03', na=False) | (database_df['mobile_number'].astype(str).str.len() > 11), 'mobile_number'] = None
        # Close the database connection
        conn.close()

        filename = file.filename

        # Check the file extension
        if filename.endswith('.csv'):
            # Read CSV file
            employee_df = pd.read_csv(file)
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            # Read Excel file
            employee_df = pd.read_excel(file)
        else:
            raise ValueError('Invalid file format. Only CSV, XLSX, and XLS are supported.')
        last_employee_id = get_last_fos_id()

        # Add a new column 'employee_id' to the DataFrame and generate employee IDs
        employee_df['employee_id'] = employee_df.apply(lambda row: generate_employee_ids(row, last_employee_id), axis=1)
        employee_df['mobile_number'] = employee_df['mobile_number'].astype(str)
        employee_df['mobile_number'] = employee_df['mobile_number'].apply(update_mobile_number)
        employee_df['mobile_number'] =  pd.to_numeric(employee_df['mobile_number'], errors='coerce').astype('Int64')
        employee_df['mobile_number'] = employee_df['mobile_number'].astype(str)
        employee_df['employee_name'] = employee_df['employee_name'].str.lower()
        employee_df.loc[~employee_df['mobile_number'].astype(str).str.startswith('923', na=False) | (employee_df['mobile_number'].astype(str).str.len() > 12), 'mobile_number'] = None
        
        leavers_df = database_df[~(database_df['employee_name'].isin(employee_df['employee_name']) & 
                            database_df['cnic_no'].isin(employee_df['cnic_no']))]
        leavers_df['employee_name'] = leavers_df['employee_name'].str.title()
        leavers_df.to_excel('dec_leavers_df.xlsx',index=False)

        joiners_df = employee_df[~(employee_df['employee_name'].isin(database_df['employee_name']) & 
                                employee_df['cnic_no'].isin(database_df['cnic_no']))]
        joiners_df['employee_name'] = joiners_df['employee_name'].str.title()
        joiners_df.to_excel('dec_joiners_df.xlsx',index=False)
        
        merged_df = pd.merge(database_df, employee_df, on=['employee_name', 'cnic_no'], suffixes=('_nov', '_dec'))
        transfer_df = merged_df[merged_df['office_id_nov'] != merged_df['office_id_dec']]
        transfer_df.to_excel('transfer_cases.xlsx',index=False)
        
        merged_df = employee_df.merge(database_df, on=['employee_name','cnic_no'], how='left', suffixes=('_dec', '_nov'))
        employee_df['mobile_number'] = employee_df['mobile_number'].fillna(merged_df['mobile_number_nov'])
        employee_df['employee_name'] = employee_df['employee_name'].str.title()
        employee_df.to_excel('updated_employee_data.xlsx',index=False)
    except Exception as e:
        print(str(e))
        raise ValueError(str(e))

def update_employee_left_in_database(employee_ids):
    try:
        # Get current Pakistani time
        pk_timezone = pytz.timezone('Asia/Karachi')
        current_pk_time = datetime.now(pk_timezone)

        connection = get_retryable_connection('personal')
        cursor = connection.cursor()

        # Updated query to include employee_left_date
        update_query = """
            UPDATE employees
            SET 
                employee_left = True,
                employee_left_date = %s
            WHERE employee_id IN {}
        """

        # Create placeholders for employee_ids
        placeholders = ', '.join(['%s'] * len(employee_ids))
        formatted_query = update_query.format(f'({placeholders})')

        # Add current_pk_time as the first parameter, followed by employee_ids
        cursor.execute(formatted_query, (current_pk_time,) + tuple(employee_ids))

        connection.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()

def insert_employees_to_database():
    employees_df = pd.read_excel('employees.xlsx')
    conn = get_retryable_connection('admin')
    cursor = conn.cursor()
    employees_df.fillna(value='', inplace=True)  # Replace with empty strings
    employees_df = employees_df.dropna()

    for index, row in employees_df.iterrows():
        employee_id = row['employee_id']

        # Check if employee_id already exists in the database
        cursor.execute("SELECT COUNT(*) FROM employees WHERE employee_id = %s", (employee_id,))
        count = cursor.fetchone()[0]

        if count == 0:  # Employee ID doesn't exist, insert the row
            entry_date_str = row['entry_date'].strftime("%Y-%m-%d %H:%M:%S")  # Format for MySQL

            # Include 'employee_left' column with value True
            cursor.execute("INSERT INTO employees (employee_id, employee_name, worker_type, department, designation, mobile_number, gender, office_id, entry_date, cnic_no, employee_left) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (employee_id, row['employee_name'], row['worker_type'], row['department'],
                            row['designation'], row['mobile_number'], row['gender'], row['office_id'],
                            entry_date_str, row['cnic_no'], True))  # Set employee_left to True

            print(employee_id)
            conn.commit()

    # Commit changes and close the cursor
    conn.close()

def update_cnic_numbers():
    # Connect to the SQLite database
    conn = get_retryable_connection('admin')
    cursor = conn.cursor()
    # Read the CSV file with updated CNIC numbers into a DataFrame
    updated_cnic_df = pd.read_excel('updated_employee_cnic.xlsx')
    count = 0
    # Iterate over rows in the DataFrame and update the database
    for index, row in updated_cnic_df.iterrows():
        employee_id = row['employee_id']
        cnic_no = row['cnic_no']
        count+=1
        # Update the database for NULL or empty string CNIC numbers
        update_query = "UPDATE employees SET cnic_no = %s WHERE employee_id = %s AND (cnic_no IS NULL OR cnic_no = '');"
        cursor.execute(update_query, (cnic_no, employee_id))
        conn.commit()
    print(count)
    # Commit the changes and close the connection
    conn.close()

def insert_complaints_to_database():
    complaints_df = pd.read_excel('complaints.xlsx')  # Adjust the file path as needed
    conn = get_retryable_connection('admin')
    cursor = conn.cursor()
    # List of date columns to be converted
    date_columns = [
        'date_entry', 'in_process_date',
        'capa_date', 'rca_date', 'closed_date',
        'bounced_date', 'capa1_date', 'capa2_date', 'capa3_date',
        'rca1_date', 'rca2_date', 'rca3_date', 'bounced1_date',
        'bounced2_date', 'bounced3_date', 'capa1_date', 'capa2_date',
        'capa3_date', 'rca1_date', 'rca2_date', 'rca3_date',
        'completed_date', 'unclosed_date', 'rca_deadline',
        'rca1_deadline', 'rca2_deadline'
    ]
    for index, row in complaints_df.iterrows():
        ticket_number = row['ticket_number']

        # Check if ticket_number already exists in the database
        cursor.execute("SELECT COUNT(*) FROM complaints WHERE ticket_number = %s", (ticket_number,))
        count = cursor.fetchone()[0]

        if count == 0:  # Ticket number doesn't exist, insert the row
            # Convert date columns to the desired format
            for date_column in date_columns:
                if pd.isna(row[date_column]):
                    row[date_column] = None  # Replace with NULL
                else:
                    print(ticket_number,date_column,row[date_column])
                    row[date_column] = pd.to_datetime(row[date_column]).strftime('%Y-%m-%d %H:%M:%S')
            if pd.notna(row['date_of_issue']):  # Check if it's not null
                row['date_of_issue'] = pd.to_datetime(row['date_of_issue']).strftime('%Y-%m-%d')
            for col in row.index:
                if col not in date_columns:
                    row[col] = '' if pd.isna(row[col]) else row[col]  # Replace NaN with empty string

            cursor.execute("""
                INSERT INTO complaints (
                    complaint_no,
                    ticket_number,
                    reference_number,
                    is_urgent,
                    is_anonymous,
                    mobile_number,
                    date_of_issue,
                    complaint_categories,
                    additional_comments,
                    person_issue,
                    concerned_department,
                    previous_history,
                    proposed_solution,
                    date_entry,
                    status,
                    in_process_date,
                    capa_date,
                    rca_date,
                    capa,
                    rca,
                    closed_date,
                    bounced_date,
                    capa1_date,
                    capa2_date,
                    capa3_date,
                    rca1_date,
                    rca2_date,
                    rca3_date,
                    bounced1_date,
                    bounced2_date,
                    bounced3_date,
                    capa1,
                    capa2,
                    capa3,
                    rca1,
                    rca2,
                    rca3,
                    completed_date,
                    unclosed_date,
                    rca_deadline,
                    rca1_deadline,
                    rca2_deadline,
                    feedback,
                    feedback1,
                    lodged_by_agent
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, row.to_list())
            conn.commit()
            print(ticket_number)
            print(f"Inserted complaint with ticket_number: {ticket_number}")

    # Close the cursor and connection
    cursor.close()
    conn.close()
    
def update_employees_data():
    # Connect to MySQL database
    connection = get_retryable_connection('admin')
    cursor = connection.cursor()

    # Read data from MySQL database
    query = "SELECT * FROM employees"
    db_data = pd.read_sql(query, connection)
    print(len(db_data))
    # Read data from CSV file
    csv_data = pd.read_excel('new_data.xlsx')
    new_records = csv_data[~csv_data['employee_id'].isin(db_data['employee_id'])]
    # Update existing records
    merged_data = pd.merge(db_data, csv_data, on='employee_id', how='inner', suffixes=('_db', '_csv'))
    print(len(merged_data))
    print(len(new_records))
    records_to_delete = db_data[~db_data['employee_id'].isin(csv_data['employee_id'])]
    print(len(records_to_delete))
    for index, row in merged_data.iterrows():
        if not pd.isnull(row['employee_id']):
            update_query = "UPDATE employees SET \
                            employee_name = %s, \
                            mobile_number = %s, \
                            designation = %s, \
                            worker_type = %s, \
                            department = %s, \
                            gender = %s, \
                            office_id = %s \
                            WHERE employee_id = %s"

            # Check for NaN values and replace with None
            params = (
                row['employee_name_csv'] if not pd.isnull(row['employee_name_csv']) else None,
                row['mobile_number_csv'] if not pd.isnull(row['mobile_number_csv']) else None,
                row['designation_csv'] if not pd.isnull(row['designation_csv']) else None,
                row['worker_type_csv'] if not pd.isnull(row['worker_type_csv']) else None,
                row['department_csv'] if not pd.isnull(row['department_csv']) else None,
                row['gender_csv'] if not pd.isnull(row['gender_csv']) else None,
                int(row['office_id_csv']) if not pd.isnull(row['office_id_csv']) else None,
                int(row['employee_id'])
            )
            cursor.execute(update_query, params)
            connection.commit()

    # Insert new records
    for _, new_row in new_records.iterrows():
        if not pd.isnull(new_row['employee_id']):
            cond = True
            while cond:
                try:
                    insert_query = "INSERT INTO employees \
                                    (employee_id, employee_name, mobile_number, designation, worker_type, department, gender, office_id) \
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

                    # Check for NaN values and replace with None
                    params = (
                        int(new_row['employee_id']),
                        new_row['employee_name'] if not pd.isnull(new_row['employee_name']) else None,
                        new_row['mobile_number'] if not pd.isnull(new_row['mobile_number']) else None,
                        new_row['designation'] if not pd.isnull(new_row['designation']) else None,
                        new_row['worker_type'] if not pd.isnull(new_row['worker_type']) else None,
                        new_row['department'] if not pd.isnull(new_row['department']) else None,
                        new_row['gender'] if not pd.isnull(new_row['gender']) else None,
                        int(new_row['office_id']) if not pd.isnull(new_row['office_id']) else None
                    )

                    cursor.execute(insert_query, params)
                    connection.commit()
                    cond = False
                    print(params)
                except Exception as e:
                    print(e)
                    if 'Duplicate entry' in e:
                        new_row['employee_id'] = int(new_row['employee_id']) +1

    # Delete records not present in the CSV file
    for _, delete_row in records_to_delete.iterrows():
        delete_query = "DELETE FROM employees WHERE employee_id = %s"
        cursor.execute(delete_query, (int(delete_row['employee_id']),))
        connection.commit()

    # Close the connection
    cursor.close()
    connection.close()
def add_notifications(message, user_id):
    try:
        conn = get_retryable_connection('io')
        cursor = conn.cursor()
        sql = "INSERT INTO notifications (message, user_id) VALUES (%s, %s)"
        val = (message, user_id)
        cursor.execute(sql, val)
        conn.commit()
        return True
    except mysql.connector.Error as error:
        # Handle any MySQL errors
        print(f"MySQL Error: {error}")
        return False
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {e}")
        return False
    finally:
        # Close the connection in the end, regardless of success or failure
        if conn:
            conn.close()
            return True

def add_notifications_for_late_capas():
    try:
        # Get the ticket_number and office_id for all complaints where the CAPA deadline has passed
        conn = get_retryable_connection('io')
        cursor = conn.cursor()
        sql = "SELECT complaints.ticket_number, offices.office_id,offices.app_token FROM complaints JOIN employees ON complaints.reference_number = employees.employee_id JOIN offices ON offices.office_id = employees.office_id WHERE (rca_deadline < CURRENT_DATE() AND DATEDIFF(CURRENT_DATE(), rca_deadline) > 1) OR (rca1_deadline < CURRENT_DATE() AND DATEDIFF(CURRENT_DATE(), rca1_deadline) > 1) OR (rca2_deadline < CURRENT_DATE() AND DATEDIFF(CURRENT_DATE(), rca2_deadline) > 1)"
        cursor.execute(sql)
        results = cursor.fetchall()

        # Add a notification for each user
        for result in results:
            message = f"Your complaint ticket #{result[0]} CAPA deadline has been passed. Please submit your CAPA asap."
            user_id = result[1]
            add_notifications(message, user_id)
            if result[2]:
                send_capa_deadline_notification(result[2],result[0])

        # Close the connection
        conn.close()
        print('CAPA DEADLINE messages are sent')
    except Exception as e:
        print(f"Failed to add notifications for late CAPAs: {e}")
def send_capa_deadline_notification(app_token, ticket_number):
    EXPO_PUSH_ENDPOINT = 'https://exp.host/--/api/v2/push/send'
    payload = {
        'to': app_token,
        'sound': 'default',
        'title': 'New Complaint Registered',
        'body': f"Your complaint ticket #{ticket_number} CAPA deadline has been passed. Please submit your CAPA asap.",
        'data': {'ticket_number': ticket_number}
    }

    try:
        response = requests.post(EXPO_PUSH_ENDPOINT, json=payload)
        if response.status_code == 200:
            print('Notification sent successfully!')
        else:
            print('Error sending notification:', response.status_code)
    except Exception as e:
        print('Error sending notification:', str(e))
def get_notifications(user_id):
    try:
        conn = get_retryable_connection('io')
        cursor = conn.cursor()
        if user_id == 70:
            sql = "SELECT * FROM notifications WHERE user_id IN (60,61,62,63,64, 65, 66, 67, 68, 69, 70, 71,221,222,223) ORDER BY id DESC LIMIT 20"
            val = ()
            cursor.execute(sql, val)
        elif user_id == 73:
            sql = "SELECT * FROM notifications n LEFT JOIN offices o ON n.user_id = o.office_id JOIN employees e ON o.office_id = e.office_id JOIN complaints c ON e.employee_id = c.reference_number WHERE n.user_id BETWEEN 72 AND 110 AND c.complaint_categories != 'Workplace Health, Safety and Environment' and e.temp_data = 'Corporate Office Raya' ORDER BY id DESC LIMIT 20"
            val = ()
            cursor.execute(sql, val)
        elif user_id == 74:
            sql = "SELECT * FROM notifications n LEFT JOIN offices o ON n.user_id = o.office_id JOIN employees e ON o.office_id = e.office_id JOIN complaints c ON e.employee_id = c.reference_number WHERE n.user_id BETWEEN 72 AND 110 AND c.complaint_categories != 'Workplace Health, Safety and Environment' and e.temp_data IN ('Manga Plant','(QAIE) Plant','Kamahan','Muridke Plant') ORDER BY id DESC LIMIT 20"
            val = ()
            cursor.execute(sql, val)
        elif user_id == 75:
            sql = "SELECT * FROM notifications n LEFT JOIN offices o ON n.user_id = o.office_id JOIN employees e ON o.office_id = e.office_id JOIN complaints c ON e.employee_id = c.reference_number WHERE n.user_id BETWEEN 72 AND 110 AND c.complaint_categories != 'Workplace Health, Safety and Environment' and e.temp_data NOT IN ('Corporate Office Raya','Manga Plant','(QAIE) Plant','Kamahan','Muridke Plant') ORDER BY id DESC LIMIT 20"
            val = ()
            cursor.execute(sql, val)
        elif user_id == 76:
            sql = "SELECT * FROM notifications n LEFT JOIN offices o ON n.user_id = o.office_id JOIN employees e ON o.office_id = e.office_id JOIN complaints c ON e.employee_id = c.reference_number WHERE n.user_id BETWEEN 72 AND 110 AND c.complaint_categories = 'Workplace Health, Safety and Environment' ORDER BY id DESC LIMIT 20"
            val = ()
            cursor.execute(sql, val)
        elif user_id == 139:
            sql = "SELECT * FROM notifications WHERE user_id IN (124,125,127,131,128,132,133,139) ORDER BY id DESC LIMIT 20"
            val = ()
            cursor.execute(sql, val)
        elif user_id == 134:
            sql = "SELECT * FROM notifications WHERE user_id IN (134, 135, 136, 123, 126, 129, 130) ORDER BY id DESC LIMIT 20;"
            val = ()
            cursor.execute(sql, val)
        elif user_id == 137:
            sql = "SELECT * FROM notifications WHERE user_id IN (137,138,140) ORDER BY id DESC LIMIT 20;"
            val = ()
            cursor.execute(sql, val)
        elif user_id == 146:
            sql = """SELECT * FROM notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            WHERE (e.office_id BETWEEN 146 AND 179 AND LOWER(e.gender) = 'female' AND c.status NOT IN ('Unapproved','Rejected') AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%')
            OR (c.complaint_categories = 'Harassment' AND LOWER(c.additional_comments) LIKE '%harassment issue%' AND e.office_id BETWEEN 146 AND 179 
            AND c.status NOT IN ('Unapproved','Rejected') AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%')
            ORDER BY n.id DESC LIMIT 20;"""
            val = ()
            cursor.execute(sql, val)
        elif user_id == 147:
            sql = """SELECT * FROM notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            WHERE (e.office_id BETWEEN 146 AND 179 
            AND LOWER(e.gender) = 'male' 
            AND c.status NOT IN ('Unapproved', 'Rejected')
            AND c.reference_number BETWEEN 15100 AND 153178
            AND c.complaint_categories != 'Harassment' AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%')
        OR (c.complaint_categories = 'Harassment' 
            AND LOWER(c.additional_comments) NOT LIKE '%harassment issue%' 
            AND e.office_id BETWEEN 146 AND 179 
            AND c.status NOT IN ('Unapproved', 'Rejected')
            AND c.reference_number BETWEEN 15100 AND 153178 AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%')
            ORDER BY n.id DESC LIMIT 20;"""
            val = ()
            cursor.execute(sql, val)
        elif user_id == 148:
            sql = """SELECT * FROM notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            WHERE (e.office_id BETWEEN 146 AND 179 
            AND LOWER(e.gender) = 'male' 
            AND c.status NOT IN ('Unapproved', 'Rejected') 
            AND c.reference_number BETWEEN 153178 AND 158976
            AND c.complaint_categories != 'Harassment' AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%')
        OR (c.complaint_categories = 'Harassment' 
            AND LOWER(c.additional_comments) NOT LIKE '%harassment issue%' 
            AND e.office_id BETWEEN 146 AND 179 
            AND c.status NOT IN ('Unapproved', 'Rejected')
            AND c.reference_number BETWEEN 153178 AND 158976 AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%')
            ORDER BY n.id DESC LIMIT 20;"""
            val = ()
            cursor.execute(sql, val)
        elif user_id == 149:
            sql = """SELECT * FROM notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            WHERE e.office_id BETWEEN 146 AND 179 AND c.status NOT IN ('Unapproved','Rejected')
            AND LOWER(c.additional_comments) LIKE '%dormitory complaint%'
            ORDER BY n.id DESC LIMIT 20;"""
            val = ()
            cursor.execute(sql, val)
        elif user_id == 181:
            sql = """SELECT * FROM notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            WHERE e.office_id BETWEEN 181 AND 187 AND c.status NOT IN ('Unapproved','Rejected')
            ORDER BY n.id DESC LIMIT 20;"""
            val = ()
            cursor.execute(sql, val)
        elif user_id == 199:
            sql = """SELECT * FROM notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            WHERE e.office_id BETWEEN 199 AND 200 AND c.status NOT IN ('Unapproved','Rejected')
            ORDER BY n.id DESC LIMIT 20;"""
            val = ()
            cursor.execute(sql, val)
        elif user_id == 212:
            sql = """SELECT * FROM notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            WHERE e.office_id BETWEEN 212 AND 220 AND LOWER(e.gender) = 'male' AND c.status NOT IN ('Unapproved','Rejected')
            ORDER BY n.id DESC LIMIT 20;"""
            val = ()
            cursor.execute(sql, val)
        elif user_id == 213:
            sql = """SELECT * FROM notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            WHERE e.office_id BETWEEN 212 AND 220 AND LOWER(e.gender) = 'female' AND c.status NOT IN ('Unapproved','Rejected')
            ORDER BY n.id DESC LIMIT 20;"""
            val = ()
            cursor.execute(sql, val)
        else:
            sql = "SELECT * FROM notifications WHERE user_id = %s ORDER BY id DESC LIMIT 20"
            val = (user_id,)
            cursor.execute(sql, val)
        result = cursor.fetchall()
        return result  # You might want to process this data further depending on your requirements
    except mysql.connector.Error as error:
        # Handle any MySQL errors
        print(f"MySQL Error: {error}")
        return None  # Return None or an empty list, depending on your error handling strategy
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {e}")
        return None  # Return None or an empty list, depending on your error handling strategy
    finally:
        # Close the connection in the end, regardless of success or failure
        if conn:
            conn.close()

def update_notifications(user_id):
    try:
        conn = get_retryable_connection('io')
        cursor = conn.cursor()
        if user_id == '70':
            print('Notification updated for user_id',user_id)
            sql = "UPDATE notifications SET is_read = TRUE WHERE user_id IN (60,60,61,62,63,64, 65, 66, 67, 68, 69, 70, 71,221,222,223)"
            val = ()
            cursor.execute(sql, val)
        elif user_id == '73':
            print('Notification updated for user_id',user_id)
            sql = "UPDATE notifications n LEFT JOIN offices o ON n.user_id = o.office_id JOIN employees e ON o.office_id = e.office_id JOIN complaints c ON e.employee_id = c.reference_number  SET is_read = TRUE WHERE n.user_id BETWEEN 72 AND 110 AND c.complaint_categories != 'Workplace Health, Safety and Environment' and e.temp_data = 'Corporate Office Raya'"
            val = ()
            cursor.execute(sql, val)
        elif user_id == '74':
            print('Notification updated for user_id',user_id)
            sql = "UPDATE notifications n LEFT JOIN offices o ON n.user_id = o.office_id JOIN employees e ON o.office_id = e.office_id JOIN complaints c ON e.employee_id = c.reference_number  SET is_read = TRUE WHERE n.user_id BETWEEN 72 AND 110 AND c.complaint_categories != 'Workplace Health, Safety and Environment' and e.temp_data IN ('Manga Plant','(QAIE) Plant','Kamahan','Muridke Plant')"
            val = ()
            cursor.execute(sql, val)
        elif user_id == '75':
            print('Notification updated for user_id',user_id)
            sql = "UPDATE notifications n LEFT JOIN offices o ON n.user_id = o.office_id JOIN employees e ON o.office_id = e.office_id JOIN complaints c ON e.employee_id = c.reference_number  SET is_read = TRUE WHERE n.user_id BETWEEN 72 AND 110 AND c.complaint_categories != 'Workplace Health, Safety and Environment' and e.temp_data IN ('Manga Plant','(QAIE) Plant','Kamahan','Muridke Plant')"
            val = ()
            cursor.execute(sql, val)
        elif user_id == '76':
            print('Notification updated for user_id',user_id)
            sql = "UPDATE notifications n LEFT JOIN offices o ON n.user_id = o.office_id JOIN employees e ON o.office_id = e.office_id JOIN complaints c ON e.employee_id = c.reference_number  SET is_read = TRUE WHERE n.user_id BETWEEN 72 AND 110 AND c.complaint_categories = 'Workplace Health, Safety and Environment'"
            val = ()
            cursor.execute(sql, val)
            
        elif user_id == '139':
            print('Notification updated for user_id',user_id)
            sql = "UPDATE notifications SET is_read = TRUE WHERE user_id IN (124,125,127,131,128,132,133,139)"
            val = ()
            cursor.execute(sql, val)
        elif user_id == '134':
            print('Notification updated for user_id',user_id)
            sql = "UPDATE notifications SET is_read = TRUE WHERE user_id IN (134, 135, 136, 123, 126, 129, 130)"
            val = ()
            cursor.execute(sql, val)
        elif user_id == '137':
            print('Notification updated for user_id',user_id)
            sql = "UPDATE notifications SET is_read = TRUE WHERE user_id IN (137,138,140)"
            val = ()
            cursor.execute(sql, val)
        elif user_id == 146:
            sql = """UPDATE notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            SET n.is_read = TRUE 
            WHERE (e.office_id BETWEEN 146 AND 179 AND LOWER(e.gender) = 'female' AND c.status NOT IN ('Unapproved','Rejected') AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%')
            OR (c.complaint_categories = 'Harassment' AND LOWER(c.additional_comments) LIKE '%harassment issue%' AND e.office_id BETWEEN 146 AND 179 
            AND c.status NOT IN ('Unapproved','Rejected') AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%');
            """
            val = ()
            cursor.execute(sql, val)
        elif user_id == 147:
            sql = """UPDATE notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            SET n.is_read = TRUE 
            WHERE (e.office_id BETWEEN 146 AND 179 
            AND LOWER(e.gender) = 'male' 
            AND c.status NOT IN ('Unapproved', 'Rejected')
            AND c.reference_number BETWEEN 15100 AND 153178
            AND c.complaint_categories != 'Harassment' AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%')
        OR (c.complaint_categories = 'Harassment' 
            AND LOWER(c.additional_comments) NOT LIKE '%harassment issue%' 
            AND e.office_id BETWEEN 146 AND 179 
            AND c.status NOT IN ('Unapproved', 'Rejected')
            AND c.reference_number BETWEEN 15100 AND 153178 AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%');
            """
            val = ()
            cursor.execute(sql, val)
        elif user_id == 148:
            sql = """UPDATE notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            SET n.is_read = TRUE 
            WHERE (e.office_id BETWEEN 146 AND 179 
            AND LOWER(e.gender) = 'male' 
            AND c.status NOT IN ('Unapproved', 'Rejected') 
            AND c.reference_number BETWEEN 153178 AND 158976
            AND c.complaint_categories != 'Harassment' AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%')
        OR (c.complaint_categories = 'Harassment' 
            AND LOWER(c.additional_comments) NOT LIKE '%harassment issue%' 
            AND e.office_id BETWEEN 146 AND 179 
            AND c.status NOT IN ('Unapproved', 'Rejected')
            AND c.reference_number BETWEEN 153178 AND 158976 AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%');
            """
            val = ()
            cursor.execute(sql, val)
        elif user_id == 149:
            sql = """UPDATE notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            SET n.is_read = TRUE 
            WHERE e.office_id BETWEEN 146 AND 179 AND c.status NOT IN ('Unapproved','Rejected')
            AND LOWER(c.additional_comments) LIKE '%dormitory complaint%';
            """
            val = ()
            cursor.execute(sql, val)      
        elif user_id == 181:
            sql = """UPDATE notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            SET n.is_read = TRUE 
            WHERE (e.office_id BETWEEN 181 AND 187 AND c.status NOT IN ('Unapproved','Rejected'));
            """
            val = ()
            cursor.execute(sql, val)
        elif user_id == 199:
            sql = """UPDATE notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            SET n.is_read = TRUE 
            WHERE (e.office_id BETWEEN 199 AND 200 AND c.status NOT IN ('Unapproved','Rejected'));
            """
            val = ()
            cursor.execute(sql, val)
        elif user_id == 212:
            sql = """UPDATE notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            SET n.is_read = TRUE 
            WHERE (e.office_id BETWEEN 212 AND 220 AND LOWER(e.gender) = 'male' AND c.status NOT IN ('Unapproved','Rejected'));
            """
            val = ()
            cursor.execute(sql, val)
        elif user_id == 213:
            sql = """UPDATE notifications n 
            LEFT JOIN employees e ON e.office_id = n.user_id
            LEFT JOIN complaints c ON c.reference_number = e.employee_id
            SET n.is_read = TRUE 
            WHERE (e.office_id BETWEEN 212 AND 220 AND LOWER(e.gender) = 'female' AND c.status NOT IN ('Unapproved','Rejected'));
            """
            val = ()
            cursor.execute(sql, val)
        else:
            sql = "UPDATE notifications SET is_read = TRUE WHERE user_id = %s"
            val = (user_id,)
            cursor.execute(sql, val)
        conn.commit()
        print('Notifications Updated')
        return True  # You might want to process this data further depending on your requirements
    except mysql.connector.Error as error:
        # Handle any MySQL errors
        print(f"MySQL Error: {error}")
        return False  # Return None or an empty list, depending on your error handling strategy
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {e}")
        return False  # Return None or an empty list, depending on your error handling strategy
    finally:
        # Close the connection in the end, regardless of success or failure
        if conn:
            conn.close()    
    
def get_office_name(company_id):
    conn = get_retryable_connection('io')
    cursor = conn.cursor()

    sql_query = """
           SELECT office_name
           FROM offices
           WHERE office_id = %s
           """
    cursor.execute(sql_query, (company_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return row[0]
    return None


def get_all_buyers_data():
    conn = get_retryable_connection('admin')
    cursor = conn.cursor(buffered=True)
    
    # Fetch all buyers data
    cursor.execute("""
        SELECT
            b.buyer_id,
            b.buyer_name,
            bc.company_id,
            c.name AS company_name
        FROM
            buyers AS b
        LEFT JOIN
            buyer_company AS bc ON b.buyer_id = bc.buyer_id
        LEFT JOIN
            companies AS c ON bc.company_id = c.company_id
    """)
    buyers_data = cursor.fetchall()
    
    # Fetch all logins data
    cursor.execute("""
        SELECT access_id, email 
        FROM logins 
        WHERE role = 'admin'
    """)
    logins_data = {row[0]: row[1] for row in cursor.fetchall()}
    
    buyer_list = []
    for row in buyers_data:
        buyer_list.append({
            'buyer_id': row[0],
            'buyer_name': row[1],
            'company_id': row[2],
            'company_name': row[3],
            'username': logins_data.get(row[0], '')
        })
    
    cursor.close()
    conn.close()
    return buyer_list


def delete_buyers(buyer_id):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        cursor.execute(f"""DELETE FROM buyers WHERE buyer_id = {buyer_id}""")
        conn.commit()
        return True
    except Exception as e:
        print('Error:', e)
        return False
    finally:
        cursor.close()
        conn.close()

def get_app_token(reference_number):
    conn = get_retryable_connection('complaints')
    cursor = conn.cursor()
    try:
        cursor.execute(f"""SELECT app_token from offices where office_id in (SELECT office_id from employees where employee_id = {reference_number})""")
        token = cursor.fetchone()
        if token:
            return token[0]
        return None
    except Exception as e:
        print('Error',e)
        
def get_app_token_from_ticket(ticket_number):
    conn = get_retryable_connection('complaints')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT app_token from offices where office_id in (SELECT office_id from employees where employee_id in (Select reference_number from complaints where ticket_number=%s))", (ticket_number,))
        token = cursor.fetchone()
        if token:
            return token[0]
        return None
    except Exception as e:
        print('Error', e)

        
def get_office_id_from_ticket(ticket_number):
    conn = get_retryable_connection('complaints')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT office_id from offices where office_id in (SELECT office_id from employees where employee_id in (Select reference_number from complaints where ticket_number=%s))", (ticket_number,))
        token = cursor.fetchone()
        if token:
            return token[0]
        return None
    except Exception as e:
        print('Error', e)
def find_company_id(company_name):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    select_company_id_query = "SELECT office_id FROM offices WHERE office_name = %s"
    cursor.execute(select_company_id_query, (company_name,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]  # Return the first column of the result (company_id)
    return None

def current_pakistan_time():
        return datetime.now(pakistani_tz).strftime('%Y-%m-%d %H:%M:%S')
def approve_complaint(ticket_number):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT status FROM complaints WHERE ticket_number = %s", (ticket_number,))
        status = cursor.fetchone()
        if status:
            status = status[0]
            print('status', status.lower())

            if status.lower() == 'unapproved':
                cursor.execute(
                    "UPDATE complaints SET status = 'Unprocessed', approval_date = %s WHERE ticket_number = %s",
                    (current_pakistan_time(), ticket_number))
                conn.commit()
                return True
            else:
                return False
        else:
            print('No status found for ticket:', ticket_number)
            return False
    except Exception as e:
        print("Error", e)
        return False
    finally:
        cursor.close()
        conn.close()
def reject_complaint(ticket_number):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT status FROM complaints WHERE ticket_number = %s", (ticket_number,))
        status = cursor.fetchone()
        
        if status:
            status = status[0]

            if status.lower() == 'unapproved':
                cursor.execute(
                    "UPDATE complaints SET status = 'Rejected', rejected_date = %s WHERE ticket_number = %s",
                    (current_pakistan_time(), ticket_number))
                conn.commit()
                return True
            else:
                return False
        else:
            print('No status found for ticket:', ticket_number)
            return False
    except Exception as e:
        print("Error", e)
        return False
    finally:
        cursor.close()
        conn.close()

def bounce_complaint_action(ticket_number, feedback):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        cursor.execute(
            """SELECT c.status, c.bounced_date, c.bounced1_date,e.office_id FROM complaints c 
            LEFT JOIN employees e ON c.reference_number = e.employee_id WHERE c.ticket_number = %s""", (ticket_number,))
        result = cursor.fetchone()

        if result:
            status, bounce_date, bounced1_date,office_id = result
            print('Office ID',office_id)
            if status.lower() == 'closed':
                cursor.execute(
                    """UPDATE complaints SET status = 'Bounced', bounced_date = %s, feedback = %s WHERE ticket_number = %s""",
                    (current_pakistan_time(), feedback, ticket_number))
                if not bounce_date:
                    if office_id > 180 and office_id < 188:
                        send_bounced_complaint_email('shahzaib.abbas@johnnyandjugnu.com',ticket_number,feedback,'Shahzaib Sb')
                if bounce_date:
                    cursor.execute(
                        """UPDATE complaints SET status = 'Bounced1', bounced1_date = %s, feedback1 = %s WHERE ticket_number = %s""",
                        (current_pakistan_time(), feedback, ticket_number))
                    if office_id > 180 and office_id < 188:
                        send_bounced_complaint_email('gohar.iqbal@johnnyandjugnu.com',ticket_number,feedback,'Gohar Sb')
                        send_bounced_complaint_email('shahzaib.abbas@johnnyandjugnu.com',ticket_number,feedback,'Shahzaib Sb')
                if bounced1_date:
                    cursor.execute(
                        """UPDATE complaints SET status = 'Unclosed', unclosed_date = %s, feedback = %s WHERE ticket_number = %s""",
                        (current_pakistan_time(), feedback, ticket_number))

                conn.commit()
                return True
            else:
                return False
        return False
    except Exception as e:
        print("Error", e)
        return False
    finally:
        cursor.close()
        conn.close()

def close_complaint(ticket_number, feedback):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT status FROM complaints WHERE ticket_number = %s", (ticket_number,))
        status = cursor.fetchone()
        if status:
            status = status[0]

            if status.lower() == 'closed':
                current_time = current_pakistan_time()
                print('Current Time:', current_time)
                cursor.execute(
                    "UPDATE complaints SET status = 'Completed', close_feedback = %s, completed_date = %s WHERE ticket_number = %s",
                    (feedback, current_time, ticket_number))
                conn.commit()
                return True
            else:
                return False
        else:
            print('No status found for ticket:', ticket_number)
            return False
    except Exception as e:
        print("Error", e)
        return False
    finally:
        cursor.close()
        conn.close()


def delete_office_from_database(office_id):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        # Backup the employees of the office to be deleted into cache_employee
        sql_query = """
            INSERT INTO cache_employee 
            (
                employee_id,
                employee_name,
                worker_type,
                department,
                designation,
                mobile_number,
                gender,
                cnic_no,
                company_name
            )
            SELECT 
                e.employee_id, 
                e.employee_name, 
                e.worker_type, 
                e.department, 
                e.designation, 
                e.mobile_number, 
                e.gender, 
                e.cnic_no,
                c.name
            FROM employees AS e
            LEFT JOIN offices AS o ON e.office_id = o.office_id
            LEFT JOIN companies AS c ON o.company_id = c.company_id
            WHERE e.office_id = %s
        """
        cursor.execute(sql_query, (office_id,))

        # Delete the office
        cursor.execute(f"DELETE FROM offices WHERE office_id = {office_id}")
        conn.commit()
        return True

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        cursor.close()
        conn.close()

def create_database_tables():
    # Create the companies table
    create_companies_table = """
    CREATE TABLE IF NOT EXISTS companies (
        company_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        department_name VARCHAR(100)
    )
    """
    cursor.execute(create_companies_table)

    # Create the employees table
    create_table_query = """
     CREATE TABLE IF NOT EXISTS employees (
         employee_id INT PRIMARY KEY,
         employee_name VARCHAR(100) NOT NULL,
         worker_type VARCHAR(50) NOT NULL,
         department VARCHAR(100),
         designation VARCHAR(100),
         mobile_number VARCHAR(20),
         gender ENUM('Male', 'Female', 'N/A') NOT NULL,
         company_id INT NOT NULL,
         FOREIGN KEY (company_id) REFERENCES companies(company_id)
     )
     """
    cursor.execute(create_table_query)

    # Create the complaints table
    create_table_query = """
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_no INT AUTO_INCREMENT PRIMARY KEY,
            ticket_number VARCHAR(100),
            reference_number INT,
            is_urgent BOOLEAN,
            is_anonymous BOOLEAN,
            mobile_number VARCHAR(20),
            date_of_issue DATETIME,
            complaint_categories VARCHAR(255),
            additional_comments TEXT,
            person_issue VARCHAR(255),
            concerned_department VARCHAR(255),
            previous_history VARCHAR(255),
            proposed_solution VARCHAR(255),
            FOREIGN KEY (reference_number) REFERENCES employees(employee_id)
        )
        """
    cursor.execute(create_table_query)

def insert_complaint(data,lodged_by_agent=1):
    conn = get_retryable_connection('complaints')
    cursor = conn.cursor()
    data['lodged_by'] = lodged_by_agent

    while True:
        try:
            if data['reference_number'] == 0:
                insert_query = """
                INSERT INTO complaints (ticket_number, is_urgent, is_anonymous, mobile_number, date_of_issue, complaint_categories, additional_comments, person_issue, concerned_department, previous_history, proposed_solution, date_entry, status, lodged_by_agent)
                VALUES (%(ticket_number)s, %(is_urgent)s, %(is_anonymous)s, %(mobile_number)s, %(date_of_issue)s, %(complaint_categories)s, %(additional_comments)s, %(person_issue)s, %(concerned_department)s, %(previous_history)s, %(proposed_solution)s, %(curr_date)s, %(status)s, %(lodged_by)s)
                """
            else:
                insert_query = """
                INSERT INTO complaints (ticket_number, reference_number, is_urgent, is_anonymous, mobile_number, date_of_issue, complaint_categories, additional_comments, person_issue, concerned_department, previous_history, proposed_solution, date_entry, status, lodged_by_agent)
                VALUES (%(ticket_number)s, %(reference_number)s, %(is_urgent)s, %(is_anonymous)s, %(mobile_number)s, %(date_of_issue)s, %(complaint_categories)s, %(additional_comments)s, %(person_issue)s, %(concerned_department)s, %(previous_history)s, %(proposed_solution)s, %(curr_date)s, %(status)s, %(lodged_by)s)
                """

            cursor.execute(insert_query, data)
            conn.commit()
            break
        except Exception as e:
            print("Error:", e)
            if 'Duplicate entry' in str(e):
                # Increment the first part of the ticket number.
                data['ticket_number'] = increment_ticket_number(data['ticket_number'])
            else:
                raise e

    cursor.close()
    conn.close()
    return True

def increment_ticket_number(ticket_number):
    # Split the ticket number into two parts.
    parts = ticket_number.split('-')
    
    # Increment the first part of the ticket number.
    first_part = int(parts[0][3:])
    first_part += 1
    if first_part == 999:
        first_part = 000
    # Return the new ticket number.
    return str(parts[0][:-3]) + str(first_part) + '-' + parts[1]

def get_company_id_by_fos_id(fos_id):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        cursor.execute(f"""SELECT office_id from employees where employee_id = {fos_id}""")
        office_id = cursor.fetchone()
        if office_id:
            return office_id[0]
        else:
            return '00'

    finally:
        cursor.close()
        conn.close()

def get_buyer_name(buyer_id):
    try:
        conn = get_retryable_connection('admin')
        cursor = conn.cursor()

        # Use parameterized query to prevent SQL injection
        query = "SELECT buyer_name FROM buyers WHERE buyer_id = %s"
        cursor.execute(query, (buyer_id,))

        # Fetch the result
        buyer_name = cursor.fetchone()

        if buyer_name:
            print('buyer_name:', buyer_name[0])
            return buyer_name[0]
        else:
            print('No buyer found for the given buyer_id:', buyer_id)
            return None

    except mysql.connector.Error as e:
        print('MySQL Error:', e)
        # Handle the error as needed

    finally:
        # Close cursor and connection in the 'finally' block
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def generate_anonymous_ticket(company_id,curr_date):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        cursor.execute("""
                SELECT ticket_number
                FROM complaints
                WHERE is_anonymous = TRUE
                ORDER BY date_entry DESC
                LIMIT 1
            """)
        result = cursor.fetchone()
        if result:
            result = result[0]
            result = result[6:8]

            if result[0] == '0':
                result = int(result) + 1
                result = "0" + str(result)

            elif result == '99':
                result = '00'
            else:
                result = int(result) + 1
            if company_id == '0':
                ticket_no = f"XX{curr_date}{result}-00XXXX"
            else:
                ticket_no = f"XX{curr_date}{result}-{company_id[0:2]}XXXX"
        else:
            if company_id == '0':
                ticket_no = f"XX{curr_date}00-00XXXX"
            else:
                ticket_no = f"XX{curr_date}00-{company_id[0:2]}XXXX"
        return ticket_no
    finally:
        cursor.close()
        conn.close()

def delete_employee(employee_id):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        if employee_id is not None:
            sql_query = """
                INSERT INTO cache_employee 
                (
                    employee_id,
                    employee_name,
                    worker_type,
                    department,
                    designation,
                    mobile_number,
                    gender,
                    cnic_no,
                    company_name
                )
                SELECT 
                    e.employee_id, 
                    e.employee_name, 
                    e.worker_type, 
                    e.department, 
                    e.designation, 
                    e.mobile_number, 
                    e.gender, 
                    e.cnic_no,
                    c.name
                FROM employees AS e
                LEFT JOIN offices AS o ON e.office_id = o.office_id
                LEFT JOIN companies AS c ON o.company_id = c.company_id
                WHERE e.employee_id = %s
            """
            cursor.execute(sql_query, (employee_id,))
            delete_query = "DELETE FROM employees WHERE employee_id = %s"
            cursor.execute(delete_query, (employee_id,))
            conn.commit()

    except Exception as e:
        print("Error", e)

    finally:
        cursor.close()
        conn.close()




def add_employee_to_database(employee_data):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    try:
        # Replace NaN values with None for database insertion
        cleaned_employee_data = {k: None if pd.isna(v) else v for k, v in employee_data.items()}

        if cleaned_employee_data['location']:
            insert_query = (
                "INSERT INTO employees "
                "(employee_id, employee_name, worker_type, department, designation, mobile_number, gender, office_id, cnic_no, company_id, temp_data, entry_date)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            
            # Attempt to insert the employee data
            while True:
                try:
                    # Get the current time in the Pakistan timezone
                    pakistan_tz = pytz.timezone('Asia/Karachi')
                    entry_date = datetime.now(pakistan_tz).strftime('%Y-%m-%d %H:%M:%S')

                    cursor.execute(insert_query, (
                        cleaned_employee_data['employee_id'],
                        cleaned_employee_data['employee_name'],
                        cleaned_employee_data['worker_type'],
                        cleaned_employee_data['department'],
                        cleaned_employee_data['designation'],
                        cleaned_employee_data['mobile_number'],
                        cleaned_employee_data['gender'],
                        cleaned_employee_data['office_id'],
                        cleaned_employee_data['cnic_no'],
                        cleaned_employee_data['company_id'],
                        cleaned_employee_data['location'],
                        entry_date
                    ))
                    conn.commit()
                    break  # Exit the loop if insertion is successful
                except mysql.connector.IntegrityError as e:
                    if e.errno == 1062:  # Duplicate entry error
                        cleaned_employee_data['employee_id'] += 1
                        temp = str(cleaned_employee_data['employee_id'])
                        if temp[-4] == '9' and temp[-1] == '9' and temp[-2] == '9' and temp[-3] == '9':
                            temp = temp[0:3] + '0000'
                        cleaned_employee_data['employee_id'] = int(temp)
                    else:
                        print("Error occurred during insertion:", e)
                        break  # Exit the loop on other errors
                except Exception as e:
                    print("Error occurred during insertion:", e, cleaned_employee_data)
        else:
            insert_query = (
                "INSERT INTO employees "
                "(employee_id, employee_name, worker_type, department, designation, mobile_number, gender, office_id, cnic_no, company_id, entry_date)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
    
            # Attempt to insert the employee data
            while True:
                try:
                    # Get the current time in the Pakistan timezone
                    pakistan_tz = pytz.timezone('Asia/Karachi')
                    entry_date = datetime.now(pakistan_tz).strftime('%Y-%m-%d %H:%M:%S')

                    cursor.execute(insert_query, (
                        cleaned_employee_data['employee_id'],
                        cleaned_employee_data['employee_name'],
                        cleaned_employee_data['worker_type'],
                        cleaned_employee_data['department'],
                        cleaned_employee_data['designation'],
                        cleaned_employee_data['mobile_number'],
                        cleaned_employee_data['gender'],
                        cleaned_employee_data['office_id'],
                        cleaned_employee_data['cnic_no'],
                        cleaned_employee_data['company_id'],
                        entry_date
                    ))
                    conn.commit()
                    break  # Exit the loop if insertion is successful
                except mysql.connector.IntegrityError as e:
                    if e.errno == 1062:  # Duplicate entry error
                        cleaned_employee_data['employee_id'] += 1
                        temp = str(cleaned_employee_data['employee_id'])
                        if temp[-4] == '9' and temp[-1] == '9' and temp[-2] == '9' and temp[-3] == '9':
                            temp = temp[0:3] + '0000'
                        cleaned_employee_data['employee_id'] = int(temp)
                    else:
                        print("Error occurred during insertion:", e)
                        break  # Exit the loop on other errors
                except Exception as e:
                    print("Error occurred during insertion:", e, cleaned_employee_data)
        return True

    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return False

    finally:
        cursor.close()
        conn.close()


def get_all_company_data():
    conn = get_retryable_connection('io')
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("""
        SELECT
            c.company_id,
            c.name AS company_name,
            CAST(SUM(office_employee_count.num_employees) AS SIGNED) AS total_employees,
            COUNT(o.office_id) AS num_offices,
            CAST(SUM(office_complaint_count.num_complaints) AS SIGNED) AS num_complaints
        FROM
            companies c
        LEFT JOIN
            offices o ON c.company_id = o.company_id
        LEFT JOIN
            (
                SELECT
                    e.office_id,
                    COUNT(e.employee_id) AS num_employees
                FROM
                    employees e
                GROUP BY
                    e.office_id
            ) office_employee_count ON o.office_id = office_employee_count.office_id
        LEFT JOIN
            (
                SELECT
                    e.office_id,
                    COUNT(cm.complaint_no) AS num_complaints
                FROM
                    complaints cm
                LEFT JOIN employees e ON e.employee_id = cm.reference_number
                GROUP BY
                    e.office_id
            )
            office_complaint_count ON o.office_id = office_complaint_count.office_id
        GROUP BY
            c.company_id, c.name;
        """)
        data = cursor.fetchall()
        company_data_list = []
        for row in data:
            email = ''
            print('Buyer Data: ', row)
            buyer_name = row[1]
            cursor.execute("SELECT buyer_id FROM buyers WHERE buyer_name = %s", (buyer_name,))
            buyer_id_result = cursor.fetchall()
            print('Buyer ID: ', buyer_id_result)
            if buyer_id_result:
                cursor.execute("""SELECT id, email FROM logins WHERE access_id = %s AND role = 'admin'""", (buyer_id_result[0][0],))
                login_data = cursor.fetchall()
                if login_data:
                    email = login_data[0][1]
            company_dict = {
                "company_id": row[0],
                "name": row[1],
                "employees_count": row[2],
                "office_count": row[3],
                "complaint_count": row[4],
                'username': email
            }
            company_data_list.append(company_dict)
        return company_data_list
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()
def delete_company_data(data):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        sql_query = """
            INSERT INTO cache_employee 
            (
                employee_id,
                employee_name,
                worker_type,
                department,
                designation,
                mobile_number,
                gender,
                cnic_no,
                company_name
            )
            SELECT 
                e.employee_id, 
                e.employee_name, 
                e.worker_type, 
                e.department, 
                e.designation, 
                e.mobile_number, 
                e.gender, 
                e.cnic_no,
                c.name
            FROM employees AS e
            LEFT JOIN offices AS o ON e.office_id = o.office_id
            LEFT JOIN companies AS c ON o.company_id = c.company_id
            WHERE c.company_id = %s
        """
        cursor.execute(sql_query, (data,))

        cursor.execute("SELECT id from logins where access_id = %s and role='admin'", (data,))
        id = cursor.fetchone()

        if id:
            id = id[0]
            cursor.execute("DELETE from logins where access_id = %s and role='admin'", (data,))

        cursor.execute("SELECT name from companies where company_id = %s", (data,))
        company_name = cursor.fetchone()[0]

        cursor.execute("DELETE FROM buyer_company WHERE company_id = %s", (data,))
        cursor.execute("DELETE from buyers where buyer_name = %s", (company_name,))
        cursor.execute("DELETE FROM companies WHERE company_id = %s", (data,))

        conn.commit()
        return True
    except Exception as e:
        print("Error updating company data:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def fetch_all_cache_employee_data():
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        # SQL query to retrieve all data from the "cache_employee" table
        sql_query = """
            SELECT employee_id, employee_name, worker_type, department, 
                   designation, mobile_number, gender, company_name, cnic_no
            FROM cache_employee
        """
        cursor.execute(sql_query)

        # Fetch all rows from the result
        rows = cursor.fetchall()

        # Create a list of dictionary for the result set
        result = []
        for row in rows:
            result.append({
                "employee_id": row[0],
                "employee_name": row[1],
                "worker_type": row[2],
                "department": row[3],
                "designation": row[4],
                "mobile_number": row[5],
                "gender": row[6],
                "company_name": row[7],
                "cnic_no": row[8]
            })

        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()


def update_company_data(data):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        query = "UPDATE companies SET name = %s WHERE company_id = %s"
        values = (data['name'], data['company_id'])
        password = data['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cursor.execute(query, values)
        conn.commit()

        cursor.execute("SELECT buyer_id from buyers WHERE buyer_name = %s", (data['name'],))
        buyer_id = cursor.fetchone()

        if buyer_id:
            access_id = buyer_id[0]

            # Update logins table with hashed password
            logins_query = "UPDATE logins SET password = %s, email = %s WHERE access_id = %s and role = 'admin'"
            cursor.execute(logins_query, (hashed_password, data['username'], access_id))

            conn.commit()
            return True
    except Exception as e:
        print("Error updating company data:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def fetch_company_names():
    conn = get_retryable_connection('complaints')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT office_name FROM offices")
        company_names = [row[0] for row in cursor.fetchall()]
        return company_names
    except Exception as e:
        print('Error fetching data:', e)
        return []
    finally:
        cursor.close()
        conn.close()


def get_all_complaints_data():
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        sql = "SELECT * FROM complaints"
        cursor.execute(sql)
        complaints = cursor.fetchall()
        return complaints
    except Exception as e:
        print("Error:", e)
        return []
    finally:
        cursor.close()
        conn.close()
        
        
def get_io_phone_no(fos_id, category, complaint_text = ''):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    try:
        if str(fos_id).startswith(('86', '87', '88')):
            sql = f"SELECT mobile_number, office_id FROM offices WHERE office_id IN (SELECT office_id FROM employees WHERE employee_id = %s)"
            cursor.execute(sql, (fos_id,))
            result = cursor.fetchone()
            sql = f"SELECT temp_data FROM employees WHERE employee_id = %s"
            cursor.execute(sql, (fos_id,))
            location = cursor.fetchone()
            if location:
                location = location[0]
            if result:
                phone_no, office_id = result
            if location == 'Corporate Office Raya' and category != 'Workplace Health, Safety and Environment':
                phone_no = '923002075544'
                return phone_no, office_id
            elif location in ('Manga Plant', '(QAIE) Plant', 'Kamahan', 'Muridke Plant') and category != 'Workplace Health, Safety and Environment':
                phone_no = '923011131521'
                return phone_no, office_id
            elif location not in ('Corporate Office Raya', 'Manga Plant', '(QAIE) Plant', 'Kamahan', 'Muridke Plant') and category != 'Workplace Health, Safety and Environment':
                phone_no = '923011131539'
                return phone_no, office_id
            elif category == 'Workplace Health, Safety and Environment':
                phone_no = '923354799949'
                return phone_no, office_id
            else:
                return phone_no, office_id
                
        if str(fos_id).startswith('45'):
            sql = f"SELECT gender, office_id FROM employees WHERE employee_id = %s"
            cursor.execute(sql, (fos_id,))
            result = cursor.fetchone()
            if result:
                gender, office_id = result
                if gender.lower() == 'female':
                    phone_no = '923443110408'
                else:  # male
                    phone_no = '923062810656'
                return phone_no, office_id

        if str(fos_id).startswith('15') and 'dormitory complaint' not in complaint_text.lower():
            sql = f"SELECT mobile_number, office_id FROM offices WHERE office_id IN (SELECT office_id FROM employees WHERE employee_id = %s)"
            cursor.execute(sql, (fos_id,))
            result = cursor.fetchone()
            if result:
                phone_no, office_id = result
            sql = f"SELECT gender FROM employees WHERE employee_id = %s"
            cursor.execute(sql, (fos_id,))
            gender = cursor.fetchone()
            if gender:
                gender = gender[0]
            if fos_id in range(151000,153179) and gender.lower() == 'male':
                phone_no = '923361916786'
            elif fos_id in range(153179,158977) and gender.lower() == 'male':
                phone_no = '923019796194'
            else:
                phone_no = '923027353971'
            return phone_no, office_id
                
        else:
            sql = f"SELECT mobile_number, office_id FROM offices WHERE office_id IN (SELECT office_id FROM employees WHERE employee_id = %s)"
            cursor.execute(sql, (fos_id,))
            result = cursor.fetchone()
            if result:
                phone_no, office_id = result
                return phone_no, office_id
            else:
                return None, None
    except Exception as e:
        print("Error:", e)
        return None, None
    finally:
        cursor.close()
        conn.close()



def get_all_offices_data():
    try:
        conn = get_retryable_connection('personal')
        cursor = conn.cursor()
        try:
            query = """
            SELECT o.office_id, o.office_name, o.office_location, o.company_id, o.mobile_number,
                   l.id as login_id, l.email, c.name as company_name
            FROM offices o
            LEFT JOIN logins l ON o.office_id = l.access_id AND l.role = 'io'
            LEFT JOIN companies c ON o.company_id = c.company_id
            """
            print("Executing Query:", query)
            cursor.execute(query)
            data = cursor.fetchall()
            office_data_list = []
            for row in data:
                office_id, office_name, office_location, company_id, mobile_number, login_id, email, company_name = row
                office_dict = {
                    'password': '',  # Assuming you don't want to include actual passwords
                    'office_id': office_id,
                    'office_name': office_name,
                    'office_location': office_location,
                    'company_id': company_id,
                    'username': email or '',  # Use empty string if email is None
                    'mobile_number': mobile_number,
                    'company_name': company_name or ''  # Use empty string if company_name is None
                }
                office_data_list.append(office_dict)
            
            print('Office List', office_data_list)
            return office_data_list
        except Exception as err:
            print("Error executing query:", err)
            print("Traceback:", traceback.format_exc())
            return None
        finally:
            cursor.close()
            conn.close()
    except Exception as conn_err:
        print("Error connecting to the database:", conn_err)
        print("Traceback:", traceback.format_exc())
        return None



def add_new_office(office_name, office_location, company_id, mobile_number):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        cursor.execute("""SELECT company_id FROM companies WHERE name = %s""", (company_id,))
        company_id = cursor.fetchone()[0]

        insert_query = "INSERT INTO offices (office_name, office_location, company_id, mobile_number) VALUES (%s, %s, %s, %s)"
        values = (office_name, office_location, company_id, mobile_number)
        cursor.execute(insert_query, values)
        conn.commit()

        cursor.execute("""SELECT office_id FROM offices WHERE company_id = %s AND office_name = %s""",
                       (company_id, office_name))
        office_id = cursor.fetchone()[0]
        office_name = office_name.split(' ', 2)[0]
        enter_login(f'{office_name}{office_id}', generate_random_password(8), 'io', office_id)

        return True
    except Exception as e:
        print('Error fetching data:', e)
        return False
    finally:
        cursor.close()
        conn.close()


def get_io_number_from_fosid(fos_id):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        cursor.execute("""SELECT mobile_number FROM offices WHERE office_id IN
        (SELECT office_id FROM offices WHERE employee_id = %s)""", (fos_id,))
        mobileNumber = cursor.fetchone()
        return mobileNumber[0] if mobileNumber else None
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        cursor.close()
        conn.close()


def update_office_data(data):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        password = data['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cursor.execute("""UPDATE offices
            SET office_name = %s, office_location = %s, mobile_number = %s
            WHERE office_id = %s""",
                       (data['office_name'], data['office_location'], data['mobile_number'], data['office_id']))
        conn.commit()

        cursor.execute("""SELECT id FROM logins WHERE access_id = %s AND role = 'io'""", (data['office_id'],))
        id = cursor.fetchone()
        print('office_idfrom login', id)
        if id:


            logins_query = """UPDATE logins SET password = %s, email = %s WHERE access_id = %s AND role = 'io'"""
            cursor.execute(logins_query, (hashed_password, data['username'], data['office_id']))

            conn.commit()
        return True
    except Exception as e:
        print('Error updating office data:', e)
        return False
    finally:
        cursor.close()
        conn.close()


def get_all_company_names():
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        cursor.execute("""SELECT name FROM companies""")
        data = cursor.fetchall()

        company_names = [{'name': row[0]} for row in data]
        return company_names
    except Exception as err:
        print("Error:", err)
        return []
    finally:
        cursor.close()
        conn.close()



import random
import string

def generate_random_password(length=10):
    if length < 4:
        raise ValueError("Password length must be at least 4")

    special_characters = "!@#$%^&*()_-+=<>?"
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits

    # Ensure at least one of each character type
    password = [
        random.choice(special_characters),
        random.choice(lowercase_letters),
        random.choice(uppercase_letters),
        random.choice(digits)
    ]

    # Generate the remaining characters
    remaining_length = length - 4

    # Use one special character, one lowercase letter, one uppercase letter,
    # and fill the rest with digits
    all_characters = lowercase_letters + uppercase_letters + digits

    # Add one of each character type and then fill the rest with random choices
    for _ in range(remaining_length):
        character_type = random.choice(["lower", "upper", "digit"])
        if character_type == "lower":
            password.append(random.choice(lowercase_letters))
        elif character_type == "upper":
            password.append(random.choice(uppercase_letters))
        else:
            password.append(random.choice(digits))

    # Shuffle the password to make the order random
    random.shuffle(password)

    # Convert the list to a string
    final_password = ''.join(password)

    return final_password


def add_new_company(company_name):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO companies (name) VALUES (%s)", (company_name,))
        cursor.execute("INSERT INTO buyers (buyer_name) VALUES (%s)", (company_name,))
        cursor.execute("SELECT buyer_id from buyers where buyer_name = %s", (company_name,))
        buyer_id = cursor.fetchone()[0]
        cursor.execute("SELECT company_id from companies where name = %s", (company_name,))
        company_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO buyer_company (buyer_id, company_id) VALUES (%s, %s)", (buyer_id, company_id))
        conn.commit()
        
        # Generate username by lowercasing and replacing spaces with underscores
        username = company_name.lower().replace(' ', '_')
        
        enter_login(username, generate_random_password(8), 'admin', buyer_id)
        return True
    except Exception as e:
        print('Error adding new company:', e)
        return False
    finally:
        cursor.close()
        conn.close()
def get_specific_complaint_data(ticket_no):
    conn = get_retryable_connection('complaints')
    cursor = conn.cursor()
    sql_query = """
           SELECT c.complaint_no,
              c.ticket_number,
              c.reference_number,
              c.is_urgent,
              c.is_anonymous,
              c.mobile_number AS complaint_mobile_number,
              c.date_of_issue,
              c.complaint_categories,
              c.additional_comments,
              c.person_issue,
              c.concerned_department,
              c.previous_history,
              c.proposed_solution,
              c.status,
              e.employee_name,
              c.date_entry,
              c.in_process_date,
              c.capa_date,
              c.rca_date,
              c.capa,
              c.rca,
              c.closed_date,
              c.bounced_date,
              c.capa1_date,
              c.capa2_date,
              c.capa3_date,
              c.rca1_date,
              c.rca2_date,
              c.rca3_date,
              c.bounced1_date,
              c.bounced2_date,
              c.bounced3_date,
              c.capa1,
              c.capa2,
              c.capa3,
              c.rca1,
              c.rca2,
              c.rca3,
              c.completed_date,
              e.gender,
              e.designation,
               c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
             c.lodged_from_web,
             c.close_feedback
           FROM complaints c
           JOIN employees e ON c.reference_number = e.employee_id
           WHERE c.ticket_number = %s AND c.status NOT IN ('Unapproved', 'Rejected');
       """

    # Execute the query with the company ID as a parameter
    cursor.execute(sql_query, (ticket_no,))

    # Fetch all the complaints
    complaint = cursor.fetchone()
    fetched_complaints = {}
    if complaint:
        complaint = list(complaint)


        # Convert the fetched complaints into a list of dictionaries


        office_name = None
        company_name = None
        designation = ''
        gender = ''
        if complaint[4] == True:
            complaint[14] = ''
            complaint[40] = ''
        else:

            cursor.execute(f"""SELECT company_id,office_name from offices WHERE office_id IN (
               SELECT office_id from employees WHERE employee_id = {complaint[2]})""")
            office_name = cursor.fetchone()

            cursor.execute(f"""SELECT name from companies WHERE company_id = {office_name[0]}""")
            office_name = office_name[1]
            company_name = cursor.fetchone()

            if company_name:
                company_name = company_name[0]
            else:
                company_name = None
        import datetime
        fetched_complaints = {
            "ticket_number": complaint[1],
            "is_urgent": complaint[3],
            "is_anonymous": complaint[4],
            "mobile_number": complaint[5],
            "date_of_issue": complaint[6].strftime('%a, %d %b %Y') if isinstance(complaint[6], datetime.datetime) else
            complaint[6],
            "complaint_categories": complaint[7],
            "additional_comments": complaint[8],
            "person_issue": complaint[9],
            "concerned_department": complaint[10],
            "previous_history": complaint[11],
            "proposed_solution": complaint[12],
            "status": complaint[13],
            "employee_name": complaint[14],
            "date_entry": complaint[15].strftime('%a, %d %b %Y %I:%M %p') if complaint[15] else None,
            "in_process_date": complaint[16].strftime('%a, %d %b %Y %I:%M %p') if complaint[16] else None,
            "capa_date": complaint[17].strftime('%a, %d %b %Y %I:%M %p') if complaint[17] else None,
            "rca_date": complaint[18].strftime('%a, %d %b %Y %I:%M %p') if complaint[18] else None,
            "capa": complaint[19],
            "rca": complaint[20],
            "closed_date": complaint[21].strftime('%a, %d %b %Y %I:%M %p') if complaint[21] else None,
            "bounced_date": complaint[22].strftime('%a, %d %b %Y %I:%M %p') if complaint[22] else None,
            "capa1_date": complaint[23].strftime('%a, %d %b %Y %I:%M %p') if complaint[23] else None,
            "capa2_date": complaint[24].strftime('%a, %d %b %Y %I:%M %p') if complaint[24] else None,
            "capa3_date": complaint[25].strftime('%a, %d %b %Y %I:%M %p') if complaint[25] else None,
            "rca1_date": complaint[26].strftime('%a, %d %b %Y %I:%M %p') if complaint[26] else None,
            "rca2_date": complaint[27].strftime('%a, %d %b %Y %I:%M %p') if complaint[27] else None,
            "rca3_date": complaint[28].strftime('%a, %d %b %Y %I:%M %p') if complaint[28] else None,
            "bounced1_date": complaint[29].strftime('%a, %d %b %Y %I:%M %p') if complaint[29] else None,
            "bounced2_date": complaint[30].strftime('%a, %d %b %Y %I:%M %p') if complaint[30] else None,
            "bounced3_date": complaint[31].strftime('%a, %d %b %Y %I:%M %p') if complaint[31] else None,
            "capa1": complaint[32],
            "capa2": complaint[33],
            "capa3": complaint[34],
            "rca1": complaint[35],
            "rca2": complaint[36],
            "rca3": complaint[37],
            'office_name': office_name,
            'company_name': company_name,
            "completed_date": complaint[38].strftime('%a, %d %b %Y %I:%M %p') if complaint[38] else None,
            'gender': complaint[39],
            'designation': complaint[40],
            'feedback':complaint[41],
            'feedback1':complaint[42],
            'capa_deadline': complaint[43].strftime('%a, %d %b %Y %I:%M %p') if complaint[43] else None,
            'capa_deadline1': complaint[44].strftime('%a, %d %b %Y %I:%M %p') if complaint[44] else None,
            'capa_deadline2': complaint[45].strftime('%a, %d %b %Y %I:%M %p') if complaint[45] else None,
            'lodged_by_agent': complaint[46],
            'lodged_from_web': complaint[47],
            'closed_feedback': complaint[48]
        }
        cursor.close()
        conn.close()
        return fetched_complaints
    return None
    

def toggle_complaint_status(ticket_number, action):
    try:
        # Establish a connection to the MySQL database
        conn = get_retryable_connection('admin')
        cursor = conn.cursor()

        # Prepare the SQL query
        query = """
        UPDATE complaints 
        SET enabled = %s 
        WHERE ticket_number = %s
        """

        # Set the enabled value based on the action
        enabled_value = 1 if action == 'enable' else 0

        # Execute the query
        cursor.execute(query, (enabled_value, ticket_number))

        # Commit the changes
        conn.commit()

        # Check if any row was affected
        if cursor.rowcount == 0:
            return False, "No complaint found with the given ticket number"

        return True, f"Complaint {ticket_number} {'enabled' if enabled_value else 'disabled'} successfully"

    except mysql.connector.Error as err:
        # Log the error (you may want to use a proper logging system)
        print(f"Database error: {err}")
        return False, "Database error occurred"

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
def fetch_survey_data(access_id=None):
    conn = get_retryable_connection('admin')
    cursor = conn.cursor(dictionary=True)
    print('Buyer_id ', access_id)
    
    survey_query = """
    SELECT DISTINCT s.id, s.title, s.description, s.created_at, s.expiry_date, question_count
    FROM surveys s
    LEFT JOIN survey_questions q ON s.id = q.survey_id
    JOIN survey_filters sf ON s.id = sf.survey_id
    JOIN employees e ON 1=1
    JOIN offices o ON e.office_id = o.office_id
    JOIN companies c ON o.company_id = c.company_id
    LEFT JOIN buyer_company ON c.company_id = buyer_company.company_id
    LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
    WHERE s.buyer_id = %s
    GROUP BY s.id;
    """
    
    cursor.execute(survey_query, (access_id,))
    surveys = cursor.fetchall()
    
    survey_data = []
    for survey in surveys:
        survey_id = survey['id']
        
        # Get total participants
        total_query = """
        SELECT DISTINCT e.employee_id, e.employee_name, e.cnic_no, o.office_name
        FROM employees e
        JOIN offices o ON e.office_id = o.office_id
        JOIN companies c ON o.company_id = c.company_id
        LEFT JOIN buyer_company bc ON c.company_id = bc.company_id
        LEFT JOIN buyers b ON bc.buyer_id = b.buyer_id
        JOIN survey_filters sf ON 
            (sf.filter_type = 'cnic' AND sf.filter_values COLLATE utf8mb4_general_ci LIKE CONCAT('%\"', e.cnic_no COLLATE utf8mb4_general_ci, '\"%'))
            OR (sf.filter_type = 'employee_id' AND sf.filter_values COLLATE utf8mb4_general_ci LIKE CONCAT('%\"', CAST(e.employee_id AS CHAR) COLLATE utf8mb4_general_ci, '\"%'))
            OR (sf.filter_type = 'employee_company_id' AND sf.filter_values COLLATE utf8mb4_general_ci LIKE CONCAT('%\"', CAST(e.company_id AS CHAR) COLLATE utf8mb4_general_ci, '\"%'))
            OR (sf.filter_type = 'department' AND sf.filter_values COLLATE utf8mb4_general_ci LIKE CONCAT('%\"', e.department COLLATE utf8mb4_general_ci, '\"%'))
            OR (sf.filter_type = 'gender' AND sf.filter_values COLLATE utf8mb4_general_ci LIKE CONCAT('%\"', e.gender COLLATE utf8mb4_general_ci, '\"%'))
            OR (sf.filter_type = 'office_id' AND sf.filter_values COLLATE utf8mb4_general_ci LIKE CONCAT('%\"', CAST(e.office_id AS CHAR) COLLATE utf8mb4_general_ci, '\"%'))
        JOIN surveys s ON s.id = sf.survey_id AND s.buyer_id = b.buyer_id
        WHERE sf.survey_id = %s;

        """
        cursor.execute(total_query, (survey_id,))
        total_participants = cursor.fetchall()
        
        # Get filled participants
        filled_query = """
        SELECT DISTINCT e.employee_id, e.employee_name, e.cnic_no, o.office_name
        FROM survey_responses sr
        JOIN employees e ON sr.employee_id = e.employee_id
        JOIN offices o ON e.office_id = o.office_id
        WHERE sr.survey_id = %s;
        """
        cursor.execute(filled_query, (survey_id,))
        filled_participants = cursor.fetchall()
        
        total_count = len(total_participants)
        filled_count = len(filled_participants)
        pending_count = total_count - filled_count

        # Prepare data for output
        total_participant_ids = set(p['employee_id'] for p in total_participants)
        filled_participant_ids = set(p['employee_id'] for p in filled_participants)

        pending_participant_data = [p for p in total_participants if p['employee_id'] not in filled_participant_ids]

        survey_data.append({
            'survey_id': survey_id,
            'title': survey['title'],
            'description': survey['description'],
            'created_at': survey['created_at'],
            'expiry_date': survey['expiry_date'],
            'question_count': survey['question_count'],
            'total_participants': total_count,
            'filled_participants': filled_count,
            'pending_participants': pending_count,
            'total_participant_data': total_participants,
            'filled_participant_data': filled_participants,
            'pending_participant_data': pending_participant_data
        })

    cursor.close()
    conn.close()
    
    return survey_data
def fetch_surveys(access_id):
    conn = None
    cursor = None
    try:
        conn = get_retryable_connection('admin')
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM surveys WHERE buyer_id = %s", (access_id,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_survey(survey_id):
    conn = None
    cursor = None
    try:
        conn = get_retryable_connection('admin')
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT s.*,b.buyer_name FROM surveys s
        JOIN buyers b ON b.buyer_id = s.buyer_id WHERE id = %s""", (survey_id,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def get_employee_stats_for_survey(survey_id):
    try:
        conn = get_retryable_connection('admin')
        cursor = conn.cursor(dictionary=True)

        # Query to check if the survey has any filters
        check_filters_query = """
        SELECT COUNT(*) AS filter_count
        FROM survey_filters
        WHERE survey_id = %s;
        """
        cursor.execute(check_filters_query, (survey_id,))
        filter_count = cursor.fetchone()['filter_count']

        if filter_count > 0:
            # Query to get total filtered employees for the specific survey
            total_filtered_query = """
          WITH filtered_employees AS (
                SELECT DISTINCT e.employee_id, e.office_id, e.cnic_no, e.department, e.gender, e.company_id, bc.buyer_id
                FROM employees e
                LEFT JOIN offices o ON e.office_id = o.office_id
                LEFT JOIN buyer_company bc ON o.company_id = bc.company_id
            ),
            survey_response_count AS (
                SELECT s.id AS survey_id, COUNT(DISTINCT sr.employee_id) AS response_count, bc.buyer_id
                FROM surveys s
                LEFT JOIN survey_responses sr ON s.id = sr.survey_id
                LEFT JOIN employees e ON sr.employee_id = e.employee_id
                LEFT JOIN offices o ON e.office_id = o.office_id
                LEFT JOIN buyer_company bc ON o.company_id = bc.company_id
                GROUP BY s.id, bc.buyer_id
            ),
            filtered_employee_count AS (
                SELECT sf.survey_id, COUNT(DISTINCT fe.employee_id) AS filtered_employee_count, fe.buyer_id
                FROM survey_filters sf
                LEFT JOIN surveys s ON sf.survey_id = s.id
                JOIN filtered_employees fe ON 
                    (sf.filter_type = 'cnic' AND sf.filter_values COLLATE utf8mb4_general_ci LIKE CONCAT('%"', fe.cnic_no COLLATE utf8mb4_general_ci, '"%'))
                    OR (sf.filter_type = 'employee_id' AND sf.filter_values COLLATE utf8mb4_general_ci LIKE CONCAT('%"', CAST(fe.employee_id AS CHAR) COLLATE utf8mb4_general_ci, '"%'))
                    OR (sf.filter_type = 'employee_company_id' AND sf.filter_values COLLATE utf8mb4_general_ci LIKE CONCAT('%"', fe.company_id COLLATE utf8mb4_general_ci, '"%'))
                    OR (sf.filter_type = 'department' AND sf.filter_values COLLATE utf8mb4_general_ci LIKE CONCAT('%"', fe.department COLLATE utf8mb4_general_ci, '"%'))
                    OR (sf.filter_type = 'gender' AND sf.filter_values COLLATE utf8mb4_general_ci LIKE CONCAT('%"', fe.gender COLLATE utf8mb4_general_ci, '"%'))
                    OR (sf.filter_type = 'office_id' AND sf.filter_values COLLATE utf8mb4_general_ci LIKE CONCAT('%"', CAST(fe.office_id AS CHAR) COLLATE utf8mb4_general_ci, '"%'))
                GROUP BY sf.survey_id, fe.buyer_id
            )
            SELECT DISTINCT s.*, 
                COALESCE(src.response_count, 0) AS response_count, 
                COALESCE(fec.filtered_employee_count, 0) AS filtered_employee_count
            FROM surveys s
            LEFT JOIN survey_filters sf ON s.id = sf.survey_id
            LEFT JOIN filtered_employees fe ON s.buyer_id = fe.buyer_id
            LEFT JOIN survey_response_count src ON s.id = src.survey_id AND s.buyer_id = src.buyer_id
            LEFT JOIN filtered_employee_count fec ON s.id = fec.survey_id AND s.buyer_id = fec.buyer_id
            LEFT JOIN buyers b ON s.buyer_id = b.buyer_id
            WHERE s.id = %s;
            """
            cursor.execute(total_filtered_query, (survey_id,))
            employee_data = cursor.fetchone()
            print('Employee Data:', employee_data)
            total_filtered = employee_data['filtered_employee_count']
            responses_count = employee_data['response_count']

            # Calculate remaining employees
            remaining_employees = total_filtered - responses_count

            return {
                'total_filtered_employees': total_filtered,
                'employees_with_responses': responses_count,
                'remaining_employees': remaining_employees
            }

        else:
            # Query to get total employees for the specific survey's buyer_id if no filters exist
            total_employees_query = """
            SELECT COUNT(e.employee_id) AS filtered_employee_count
            FROM employees e
            WHERE e.office_id IN (
                SELECT office_id
                FROM offices
                WHERE company_id IN (
                    SELECT company_id
                    FROM buyer_company
                    WHERE buyer_id IN (
                        SELECT buyer_id
                        FROM surveys
                        WHERE id = %s
                    )
                )
            );
            """
            cursor.execute(total_employees_query, (survey_id,))
            total_employees = cursor.fetchone()['filtered_employee_count']
            
            # Calculate remaining employees based on responses
            return {
                'total_filtered_employees': total_employees,
                'employees_with_responses': 0,
                'remaining_employees': total_employees
            }

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        cursor.close()
        conn.close()
def fetch_survey_questions(survey_id):
    conn = None
    cursor = None
    try:
        conn = get_retryable_connection('admin')
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM survey_questions WHERE survey_id = %s ORDER BY `order`", (survey_id,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def fetch_question_responses(survey_id, question_id):
    conn = None
    cursor = None
    try:
        conn = get_retryable_connection('admin')
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT sq.question_type, sq.options, sr.answer_text, sr.answer_option, 
                   e.employee_id, e.department, e.designation
            FROM survey_responses sr
            JOIN survey_questions sq ON sr.question_id = sq.question_id
            JOIN employees e ON sr.employee_id = e.employee_id
            WHERE sr.survey_id = %s AND sr.question_id = %s
        """, (survey_id, question_id))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def fetch_report_data(survey_id):
    survey = fetch_survey(survey_id)
    if not survey:
        return None

    # Fetch survey questions
    questions = fetch_survey_questions(survey_id)

    # Fetch responses for each question
    responses = []
    for question in questions:
        question_responses = fetch_question_responses(survey_id, question['question_id'])
        responses.append({
            'question': question,
            'responses': question_responses
        })
    
    # Get employee statistics for the survey
    employee_stats = get_employee_stats_for_survey(survey_id)

    # Prepare the report data
    report_data = {
        'survey': survey,
        'questions': questions,
        'responses': responses,
        'employee_stats': employee_stats
    }

    return report_data
def generate_report_csv(survey_id):
    # Fetch all necessary data
    report_data = fetch_report_data(survey_id)
    if not report_data:
        return None
    
    survey = report_data['survey']
    questions = report_data['questions']
    responses = report_data['responses']
    employee_stats = report_data['employee_stats']

    # Create an in-memory output file
    output = io.StringIO(newline='')
    writer = csv.writer(output)

    # Write survey information
    writer.writerow(['Survey Information'])
    writer.writerow(['ID', survey['id']])
    writer.writerow(['Title', survey['title']])
    writer.writerow(['Created At', survey['created_at']])
    writer.writerow(['Buyer Name', survey['buyer_name']])
    writer.writerow([])  # Blank line

    # Write employee statistics
    writer.writerow(['Employee Statistics'])
    writer.writerow(['Total Filtered Employees', employee_stats['total_filtered_employees']])
    writer.writerow(['Employees With Responses', employee_stats['employees_with_responses']])
    writer.writerow(['Pending Employees', employee_stats['remaining_employees']])
    writer.writerow([])  # Blank line

    # Prepare headers
    headers = ['Response Number', 'Department', 'Designation']
    for question in questions:
        headers.append(question['question_text'])
    writer.writerow(headers)

    # Prepare employee responses
    employee_responses = {}
    for question_data in responses:
        question_id = question_data['question']['question_id']
        for response in question_data['responses']:
            employee_id = response['employee_id']  # We'll use this internally but not in the output
            if employee_id not in employee_responses:
                employee_responses[employee_id] = {
                    'department': response['department'],
                    'designation': response['designation'],
                    'answers': {q['question_id']: '' for q in questions}
                }
            employee_responses[employee_id]['answers'][question_id] = response['answer_text']

    # Write employee responses
    for response_number, (employee_id, data) in enumerate(employee_responses.items(), start=1):
        row = [f"Response_{response_number}", data['department'], data['designation']]
        for question in questions:
            row.append(data['answers'][question['question_id']])
        writer.writerow(row)

    # Get the value as a UTF-8 encoded string
    return output.getvalue().encode('utf-8-sig')

def create_chart(question, responses, count_text):
    question_type = question['question_type']
    question_text = question['question_text']
    
    color_scheme = ["#072448", "#54d2d2", "#ffcb00", "#f8aa4b", "#f8aa4b"]

    calibri_path = 'static/calibri.ttf'  # Replace with the actual path to your Calibri font file
    fm.fontManager.addfont(calibri_path)
    # Try to use a system font that supports Urdu
    urdu_font = FontProperties(fname=calibri_path, size=8)
    
    # Set up right-to-left text rendering
    mpl.rcParams['axes.unicode_minus'] = False
    
    # Set the figure size to exactly 380x230 pixels
    fig = plt.figure(figsize=(600/100, 350/100), dpi=300)
    ax = fig.add_subplot(111)
    
    def prepare_rtl_text(text):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    
    if question_type in ['radio', 'select']:
        # Get all options from the question
        all_options = json.loads(question['options'])
        
        # Count responses for each option
        answer_counts = {option: 0 for option in all_options}
        for response in responses:
            answer = response['answer_text']
            if answer in answer_counts:
                answer_counts[answer] += 1
        
        labels = list(answer_counts.keys())
        values = list(answer_counts.values())
        
        small_slice_threshold = 5
        
        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct*total/100.0))
                if pct < small_slice_threshold:
                    return ''
                return f'{pct:.1f}%\n({val:d})'
            return my_autopct
        
        wedges, texts, autotexts = ax.pie(values, 
                                        autopct=make_autopct(values),
                                        colors=color_scheme,
                                        wedgeprops=dict(width=0.4), 
                                        startangle=90,
                                        pctdistance=0.75)
        
        for autotext in autotexts:
            autotext.set_fontsize(6)
            autotext.set_fontweight('bold')
            autotext.set_color('white')
        
        total = sum(values)
        small_slices = []
        
        for i, (value, wedge) in enumerate(zip(values, wedges)):
            pct = value / total * 100
            if pct < small_slice_threshold:
                ang = (wedge.theta1 + wedge.theta2) / 2
                small_slices.append((ang, pct, value, i))
        
        # Sort small slices by angle
        small_slices.sort(key=lambda x: x[0])
        
        # Function to check for label overlap
        def labels_overlap(pos1, pos2, buffer=0.1):
            return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2) < buffer
        
        label_positions = []
        
        for ang, pct, value, i in small_slices:
            radius = 1.2  # Initial radius
            rotation = 0  # Initial rotation
            
            while True:
                x = radius * np.cos(np.deg2rad(ang + rotation))
                y = radius * np.sin(np.deg2rad(ang + rotation))
                
                if not any(labels_overlap((x, y), pos) for pos in label_positions):
                    break
                
                # Alternate between increasing radius and rotating
                if rotation == 0:
                    rotation = 10  # Rotate 10 degrees clockwise
                elif rotation > 0:
                    rotation = -rotation  # Switch to counterclockwise
                else:
                    rotation = -rotation + 10  # Increase rotation and switch back to clockwise
                    radius += 0.1  # Slightly increase radius if we've tried both rotations
            
            label_positions.append((x, y))
            
            horizontalalignment = "left" if x > 0 else "right"
            connectionstyle = f"angle,angleA=0,angleB={ang + rotation}"
            
            ax.annotate(f'{pct:.1f}%\n({value:d})', 
                        xy=(np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))),
                        xytext=(x, y),
                        horizontalalignment=horizontalalignment,
                        verticalalignment="center",
                        size=6, 
                        arrowprops=dict(arrowstyle="-", connectionstyle=connectionstyle))
        
        legend_elements = [Patch(facecolor=color_scheme[i % len(color_scheme)], edgecolor='none', label=prepare_rtl_text(label)) 
                           for i, label in enumerate(labels)]
        
        ax.legend(handles=legend_elements, loc="center left", bbox_to_anchor=(1, 0.5), 
                  prop=urdu_font, fontsize=6)
    elif question_type == 'checkbox':
        # Get all options from the question
        all_options = json.loads(question['options'])
        
        # Count responses for each option
        counts = {option: sum(1 for r in responses if option in r['answer_option']) for option in all_options}
        
        labels = list(counts.keys())
        values = list(counts.values())
        
        bars = ax.barh(range(len(labels)), values, color=color_scheme)
        ax.invert_yaxis()
        
        total = sum(values)
        for i, (bar, label) in enumerate(zip(bars, labels)):
            width = bar.get_width()
            percentage = (width / total) * 100 if total > 0 else 0
            ax.text(width, bar.get_y() + bar.get_height()/2, 
                    f'{width} ({percentage:.1f}%)', 
                    ha='left', va='center', fontproperties=urdu_font,
                    fontweight='bold', fontsize=6)
            ax.text(-0.1, i, prepare_rtl_text(label), ha='right', va='center', fontproperties=urdu_font, fontsize=6)
        
        ax.set_yticks([])
    
    else:
        return None
    
    # Add count_text below the chart
    fig.text(0.5, 0.02, prepare_rtl_text(count_text), fontproperties=urdu_font, color='#2D9480', 
             fontsize=8, ha='center', va='bottom')
    
    # Adjust the layout to fit everything
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300)  # Removed bbox_inches='tight'
    img_buffer.seek(0)
    plt.close(fig)
    
    return img_buffer

def get_data_from_database_for_auditor(access_id):
    conn = get_retryable_connection('io')
    cursor = conn.cursor()
    if access_id == 15:
        sql_query = """
                SELECT c.complaint_no,
                c.ticket_number,
                c.reference_number,
                c.is_urgent,
                c.is_anonymous,
                c.mobile_number AS complaint_mobile_number,
                c.date_of_issue,
                c.complaint_categories,
                c.additional_comments,
                c.person_issue,
                c.concerned_department,
                c.previous_history,
                c.proposed_solution,
                c.status,
                e.employee_name,
                c.date_entry,
                c.in_process_date,
                c.capa_date,
                c.rca_date,
                c.capa,
                c.rca,
                c.closed_date,
                c.bounced_date,
                c.capa1_date,
                c.capa2_date,
                c.capa3_date,
                c.rca1_date,
                c.rca2_date,
                c.rca3_date,
                c.bounced1_date,
                c.bounced2_date,
                c.bounced3_date,
                c.capa1,
                c.capa2,
                c.capa3,
                c.rca1,
                c.rca2,
                c.rca3,
                c.completed_date,
                e.gender,
                e.designation,
                c.feedback,
                c.feedback1,
                c.rca_deadline,
                    c.rca1_deadline,
                    c.rca2_deadline,
                    c.lodged_by_agent,
                    c.lodged_from_web,
                    c.close_feedback,
                    c.enabled
                FROM complaints c
                JOIN employees e ON c.reference_number = e.employee_id
                WHERE e.office_id BETWEEN 146 AND 179
                AND c.status NOT IN ('Unapproved','Rejected');
                """
        cursor.execute(sql_query, ())
    elif access_id == 127:
        sql_query = """
                SELECT c.complaint_no,
                c.ticket_number,
                c.reference_number,
                c.is_urgent,
                c.is_anonymous,
                c.mobile_number AS complaint_mobile_number,
                c.date_of_issue,
                c.complaint_categories,
                c.additional_comments,
                c.person_issue,
                c.concerned_department,
                c.previous_history,
                c.proposed_solution,
                c.status,
                e.employee_name,
                c.date_entry,
                c.in_process_date,
                c.capa_date,
                c.rca_date,
                c.capa,
                c.rca,
                c.closed_date,
                c.bounced_date,
                c.capa1_date,
                c.capa2_date,
                c.capa3_date,
                c.rca1_date,
                c.rca2_date,
                c.rca3_date,
                c.bounced1_date,
                c.bounced2_date,
                c.bounced3_date,
                c.capa1,
                c.capa2,
                c.capa3,
                c.rca1,
                c.rca2,
                c.rca3,
                c.completed_date,
                e.gender,
                e.designation,
                c.feedback,
                c.feedback1,
                c.rca_deadline,
                    c.rca1_deadline,
                    c.rca2_deadline,
                    c.lodged_by_agent,
                    c.lodged_from_web,
                    c.close_feedback,
                    c.enabled
                FROM complaints c
                JOIN employees e ON c.reference_number = e.employee_id
                JOIN offices o ON e.office_id = o.office_id
                JOIN buyer_company bc ON o.company_id = bc.company_id
                WHERE bc.buyer_id = %s
                AND c.status NOT IN ('Unapproved','Rejected');
                """
        cursor.execute(sql_query, (access_id,))
    complaints_data = cursor.fetchall()
    # Execute the query with the company ID as a parameter
    
    temp_complaint = list(complaints_data)
    for i in temp_complaint:
        if not i:
            i = ''
    complaint = temp_complaint
    # Convert the fetched complaints into a list of dictionaries
    fetched_complaints = []
    for complaint in complaints_data:
        office_name = None
        company_name = None
        designation  = ''
        gender = ''
        if complaint[13] == 'Closed':
            temp_complaint = list(complaint)
            temp_complaint[13] = 'Submitted'
            complaint = temp_complaint
        if complaint[4] == True:
            temp_complaint = list(complaint)
            temp_complaint[14] = 'Anonymous'
            temp_complaint[5] = 'N/A'
            temp_complaint[40] = ''
            complaint = temp_complaint

        cursor.execute(f"""SELECT company_id,office_name from offices WHERE office_id IN (
        SELECT office_id from employees WHERE employee_id = {complaint[2]})""")
        office_name = cursor.fetchone()

        cursor.execute(f"""SELECT name from companies WHERE company_id = {office_name[0]}""")
        office_name = office_name[1]
        company_name = cursor.fetchone()

        if company_name:
            company_name = company_name[0]
        else:
            company_name = None
        fetched_complaints.append({
            "ticket_number": complaint[1],
            "is_urgent": complaint[3],
            "is_anonymous": complaint[4],
            "mobile_number": complaint[5],
            "date_of_issue": complaint[6].strftime('%a, %d %b %Y') if isinstance(complaint[6], datetime) else complaint[6],
            "complaint_categories": complaint[7],
            "additional_comments": complaint[8],
            "person_issue": complaint[9],
            "concerned_department": complaint[10],
            "previous_history": complaint[11],
            "proposed_solution": complaint[12],
            "status": complaint[13],
            "employee_name": complaint[14],
            "date_entry": complaint[15].strftime('%a, %d %b %Y %I:%M:%S %p') if complaint[15] else None,
            "in_process_date": complaint[16].strftime('%a, %d %b %Y %I:%M:%S %p') if complaint[16] else None,
            "capa_date": complaint[17].strftime('%a, %d %b %Y %I:%M:%S %p') if complaint[17] else None,
            "rca_date": complaint[18].strftime('%a, %d %b %Y %I:%M:%S %p') if complaint[18] else None,
            "capa": complaint[19],
            "rca": complaint[20],
            "closed_date": complaint[21].strftime('%a, %d %b %Y %I:%M %p') if complaint[21] else None,
            "bounced_date": complaint[22].strftime('%a, %d %b %Y %I:%M %p') if complaint[22] else None,
            "capa1_date": complaint[23].strftime('%a, %d %b %Y %I:%M %p') if complaint[23] else None,
            "capa2_date": complaint[24].strftime('%a, %d %b %Y %I:%M %p') if complaint[24] else None,
            "capa3_date": complaint[25].strftime('%a, %d %b %Y %I:%M %p') if complaint[25] else None,
            "rca1_date": complaint[26].strftime('%a, %d %b %Y %I:%M %p') if complaint[26] else None,
            "rca2_date": complaint[27].strftime('%a, %d %b %Y %I:%M %p') if complaint[27] else None,
            "rca3_date": complaint[28].strftime('%a, %d %b %Y %I:%M %p') if complaint[28] else None,
            "bounced1_date": complaint[29].strftime('%a, %d %b %Y %I:%M %p') if complaint[29] else None,
            "bounced2_date": complaint[30].strftime('%a, %d %b %Y %I:%M %p') if complaint[30] else None,
            "bounced3_date": complaint[31].strftime('%a, %d %b %Y %I:%M %p') if complaint[31] else None,
            "capa1": complaint[32],
            "capa2": complaint[33],
            "capa3": complaint[34],
            "rca1": complaint[35],
            "rca2": complaint[36],
            "rca3": complaint[37],
            'office_name':office_name,
            'company_name':company_name,
            "completed_date": complaint[38].strftime('%a, %d %b %Y %I:%M %p') if complaint[38] else None,
            'gender':complaint[39],
            'designation':complaint[40],
            'feedback':complaint[41],
            'feedback1':complaint[42],
            'capa_deadline': complaint[43].strftime('%a, %d %b %Y %I:%M %p') if complaint[43] else None,
            'capa_deadline1': complaint[44].strftime('%a, %d %b %Y %I:%M %p') if complaint[44] else None,
            'capa_deadline2': complaint[45].strftime('%a, %d %b %Y %I:%M %p') if complaint[45] else None,
            'lodged_by_agent': complaint[46],
            'lodged_from_web': complaint[47],
            'closed_feedback': complaint[48],
            'enabled': complaint[49]
        })
    cursor.close()
    conn.close()
    return fetched_complaints
def get_io_wise_complaint_count(access_id, start_date, end_date):
    result = []
    print('Start Date',start_date)
    print('End Date',end_date)
    try:
        conn = get_retryable_connection('admin')
        cursor = conn.cursor()

        if access_id in [127, 128]:
            # Query for "sadaqat139"
            io_name = "sadaqat139"
            sql_query = """
            SELECT COUNT(*) AS complaint_count
            FROM complaints c
            JOIN employees e ON c.reference_number = e.employee_id
            WHERE e.office_id IN (124, 125, 127, 131, 128, 132, 133, 139)
            AND c.status NOT IN ('Unapproved', 'Rejected')
            AND c.date_entry BETWEEN %s AND %s AND c.complaint_categories != 'Feedback';
            """
            cursor.execute(sql_query, (start_date, end_date))
            count = cursor.fetchone()[0]  # Accessing the first element of the tuple

            result.append({
                "io_name": io_name,
                "complaint_count": count
            })

            # Query for "sadaqat134"
            io_name = "sadaqat134"
            sql_query = """
            SELECT COUNT(*) AS complaint_count
            FROM complaints c
            JOIN employees e ON c.reference_number = e.employee_id
            WHERE e.office_id IN (134, 135, 136, 123, 126, 129, 130)
            AND c.status NOT IN ('Unapproved', 'Rejected')
            AND c.date_entry BETWEEN %s AND %s AND c.complaint_categories != 'Feedback';
            """
            cursor.execute(sql_query, (start_date, end_date))
            count = cursor.fetchone()[0]

            result.append({
                "io_name": io_name,
                "complaint_count": count
            })

            # Query for "sadaqat137"
            io_name = "sadaqat137"
            sql_query = """
            SELECT COUNT(*) AS complaint_count
            FROM complaints c
            JOIN employees e ON c.reference_number = e.employee_id
            WHERE e.office_id IN (137, 138, 140)
            AND c.status NOT IN ('Unapproved', 'Rejected')
            AND c.date_entry BETWEEN %s AND %s AND c.complaint_categories != 'Feedback';
            """
            cursor.execute(sql_query, (start_date, end_date))
            count = cursor.fetchone()[0]

            result.append({
                "io_name": io_name,
                "complaint_count": count
            })

    except Exception as e:
        print(f"Error in get_io_wise_complaint_count: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

    return result


def get_data_from_database(your_company_id):
    conn = get_retryable_connection('io')
    cursor = conn.cursor()
    print('company id',your_company_id)
    # SQL query to fetch data from the database
    if your_company_id == 70:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE e.office_id IN (60,61,62,63, 64, 65, 66, 67, 68, 69, 70, 71,221,222,223) AND c.status NOT IN ('Unapproved','Rejected');
        """
        cursor.execute(sql_query, ())
    elif your_company_id == 68:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE e.office_id IN (60,61,62,63, 64, 65, 66, 67, 68, 69, 70, 71,221,222,223) 
        AND c.status NOT IN ('Unapproved','Rejected')
        AND (LOWER(c.rca) LIKE '%please route this complaint to finance team%'
            OR LOWER(c.rca1) LIKE '%please route this complaint to finance team%');
        """
        cursor.execute(sql_query)
    elif your_company_id == 69:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE e.office_id IN (60,61,62,63, 64, 65, 66, 67, 68, 69, 70, 71,221,222,223) 
        AND c.status NOT IN ('Unapproved','Rejected')
        AND (LOWER(c.rca) LIKE '%please route this complaint to opertations team%'
            OR LOWER(c.rca1) LIKE '%please route this complaint to opertations team%');
        """
        cursor.execute(sql_query)
    elif your_company_id == 73:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE e.office_id BETWEEN 72 and 110 and c.complaint_categories != 'Workplace Health, Safety and Environment' and e.temp_data = 'Corporate Office Raya'  AND c.status NOT IN ('Unapproved','Rejected');
        """
        
        cursor.execute(sql_query, ())
    elif your_company_id == 74:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE e.office_id BETWEEN 72 and 110 and c.complaint_categories != 'Workplace Health, Safety and Environment' and e.temp_data IN ('Manga Plant','(QAIE) Plant','Kamahan','Muridke Plant')  AND c.status NOT IN ('Unapproved','Rejected');
        """
        
        cursor.execute(sql_query, ())
    elif your_company_id == 75:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE e.office_id BETWEEN 72 and 110 and c.complaint_categories != 'Workplace Health, Safety and Environment' and e.temp_data NOT IN ('Corporate Office Raya','Manga Plant','(QAIE) Plant','Kamahan','Muridke Plant')  AND c.status NOT IN ('Unapproved','Rejected');
        """
        cursor.execute(sql_query, ())
    elif your_company_id == 76:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE e.office_id BETWEEN 72 and 110 and c.complaint_categories = 'Workplace Health, Safety and Environment'  AND c.status NOT IN ('Unapproved','Rejected');
        """
        
        cursor.execute(sql_query, ())
    elif your_company_id == 139:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE e.office_id IN (124,125,127,131,128,132,133,139)  AND c.status NOT IN ('Unapproved','Rejected');
        """
        
        cursor.execute(sql_query, ())
    elif your_company_id == 134:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE e.office_id IN (134, 135, 136, 123, 126, 129, 130)  AND c.status NOT IN ('Unapproved','Rejected');
        """
        
        cursor.execute(sql_query, ())
    elif your_company_id == 137:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE e.office_id IN (137,138,140)  AND c.status NOT IN ('Unapproved','Rejected');
        """
        
        cursor.execute(sql_query, ())
    elif your_company_id == 146:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE (e.office_id BETWEEN 146 AND 179 AND LOWER(e.gender) = 'female' AND c.status NOT IN ('Unapproved','Rejected') AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%')
        OR (c.complaint_categories = 'Harassment' AND LOWER(c.additional_comments) LIKE '%harassment issue%' AND e.office_id BETWEEN 146 AND 179 AND c.status NOT IN ('Unapproved','Rejected') AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%');
        """
    
        cursor.execute(sql_query, ())
    elif your_company_id == 147:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE (e.office_id BETWEEN 146 AND 179 
            AND LOWER(e.gender) = 'male' 
            AND c.status NOT IN ('Unapproved', 'Rejected')
            AND c.reference_number BETWEEN 15100 AND 153178
            AND c.complaint_categories != 'Harassment' AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%')
        OR (c.complaint_categories = 'Harassment' 
            AND LOWER(c.additional_comments) NOT LIKE '%harassment issue%' 
            AND e.office_id BETWEEN 146 AND 179 
            AND c.status NOT IN ('Unapproved', 'Rejected')
            AND c.reference_number BETWEEN 15100 AND 153178 AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%');
        """
        
        cursor.execute(sql_query, ())
    elif your_company_id == 148:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE (e.office_id BETWEEN 146 AND 179 
            AND LOWER(e.gender) = 'male' 
            AND c.status NOT IN ('Unapproved', 'Rejected') 
            AND c.reference_number BETWEEN 153178 AND 158976
            AND c.complaint_categories != 'Harassment' AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%')
        OR (c.complaint_categories = 'Harassment' 
            AND LOWER(c.additional_comments) NOT LIKE '%harassment issue%' 
            AND e.office_id BETWEEN 146 AND 179 
            AND c.status NOT IN ('Unapproved', 'Rejected')
            AND c.reference_number BETWEEN 153178 AND 158976 AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%');
        """
        
        cursor.execute(sql_query, ())
    elif your_company_id == 149:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE e.office_id BETWEEN 146 AND 179 AND c.status NOT IN ('Unapproved','Rejected')
        AND LOWER(c.additional_comments) LIKE '%dormitory complaint%';
        """
    
        cursor.execute(sql_query, ())
    elif your_company_id == 181:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE e.office_id BETWEEN 181 AND 187 AND c.status NOT IN ('Unapproved','Rejected');
        """
        cursor.execute(sql_query, ())
    elif your_company_id == 199:
        sql_query = """
        SELECT c.complaint_no,
            c.ticket_number,
            c.reference_number,
            c.is_urgent,
            c.is_anonymous,
            c.mobile_number AS complaint_mobile_number,
            c.date_of_issue,
            c.complaint_categories,
            c.additional_comments,
            c.person_issue,
            c.concerned_department,
            c.previous_history,
            c.proposed_solution,
            c.status,
            e.employee_name,
            c.date_entry,
            c.in_process_date,
            c.capa_date,
            c.rca_date,
            c.capa,
            c.rca,
            c.closed_date,
            c.bounced_date,
            c.capa1_date,
            c.capa2_date,
            c.capa3_date,
            c.rca1_date,
            c.rca2_date,
            c.rca3_date,
            c.bounced1_date,
            c.bounced2_date,
            c.bounced3_date,
            c.capa1,
            c.capa2,
            c.capa3,
            c.rca1,
            c.rca2,
            c.rca3,
            c.completed_date,
            e.gender,
            e.designation,
            c.feedback,
            c.feedback1,
            c.rca_deadline,
            c.rca1_deadline,
            c.rca2_deadline,
            c.lodged_by_agent,
            c.lodged_from_web,
            c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id
        WHERE e.office_id IN (199,200) AND c.status NOT IN ('Unapproved','Rejected');
        """
        cursor.execute(sql_query, ())
    elif your_company_id == 212:
        sql_query = """
            SELECT c.complaint_no,
               c.ticket_number,
               c.reference_number,
               c.is_urgent,
               c.is_anonymous,
               c.mobile_number AS complaint_mobile_number,
               c.date_of_issue,
               c.complaint_categories,
               c.additional_comments,
               c.person_issue,
               c.concerned_department,
               c.previous_history,
               c.proposed_solution,
               c.status,
               e.employee_name,
               c.date_entry,
               c.in_process_date,
               c.capa_date,
               c.rca_date,
               c.capa,
               c.rca,
               c.closed_date,
               c.bounced_date,
               c.capa1_date,
               c.capa2_date,
               c.capa3_date,
               c.rca1_date,
               c.rca2_date,
               c.rca3_date,
               c.bounced1_date,
               c.bounced2_date,
               c.bounced3_date,
               c.capa1,
               c.capa2,
               c.capa3,
               c.rca1,
               c.rca2,
               c.rca3,
               c.completed_date,
               e.gender,
               e.designation,
               c.feedback,
               c.feedback1,
               c.rca_deadline,
                c.rca1_deadline,
                c.rca2_deadline,
                c.lodged_by_agent,
                c.lodged_from_web,
                c.close_feedback
            FROM complaints c
            JOIN employees e ON c.reference_number = e.employee_id
            WHERE e.office_id BETWEEN 212 AND 220  AND c.status NOT IN ('Unapproved','Rejected') AND e.gender = 'Male';
        """
        cursor.execute(sql_query, ())
    elif your_company_id == 213:
        sql_query = """
            SELECT c.complaint_no,
               c.ticket_number,
               c.reference_number,
               c.is_urgent,
               c.is_anonymous,
               c.mobile_number AS complaint_mobile_number,
               c.date_of_issue,
               c.complaint_categories,
               c.additional_comments,
               c.person_issue,
               c.concerned_department,
               c.previous_history,
               c.proposed_solution,
               c.status,
               e.employee_name,
               c.date_entry,
               c.in_process_date,
               c.capa_date,
               c.rca_date,
               c.capa,
               c.rca,
               c.closed_date,
               c.bounced_date,
               c.capa1_date,
               c.capa2_date,
               c.capa3_date,
               c.rca1_date,
               c.rca2_date,
               c.rca3_date,
               c.bounced1_date,
               c.bounced2_date,
               c.bounced3_date,
               c.capa1,
               c.capa2,
               c.capa3,
               c.rca1,
               c.rca2,
               c.rca3,
               c.completed_date,
               e.gender,
               e.designation,
               c.feedback,
               c.feedback1,
               c.rca_deadline,
                c.rca1_deadline,
                c.rca2_deadline,
                c.lodged_by_agent,
                c.lodged_from_web,
                c.close_feedback
            FROM complaints c
            JOIN employees e ON c.reference_number = e.employee_id
            WHERE e.office_id BETWEEN 212 AND 220  AND c.status NOT IN ('Unapproved','Rejected') AND e.gender = 'Female';
        """
        cursor.execute(sql_query, ())
    else:
        sql_query = """
            SELECT c.complaint_no,
               c.ticket_number,
               c.reference_number,
               c.is_urgent,
               c.is_anonymous,
               c.mobile_number AS complaint_mobile_number,
               c.date_of_issue,
               c.complaint_categories,
               c.additional_comments,
               c.person_issue,
               c.concerned_department,
               c.previous_history,
               c.proposed_solution,
               c.status,
               e.employee_name,
               c.date_entry,
               c.in_process_date,
               c.capa_date,
               c.rca_date,
               c.capa,
               c.rca,
               c.closed_date,
               c.bounced_date,
               c.capa1_date,
               c.capa2_date,
               c.capa3_date,
               c.rca1_date,
               c.rca2_date,
               c.rca3_date,
               c.bounced1_date,
               c.bounced2_date,
               c.bounced3_date,
               c.capa1,
               c.capa2,
               c.capa3,
               c.rca1,
               c.rca2,
               c.rca3,
               c.completed_date,
               e.gender,
               e.designation,
               c.feedback,
               c.feedback1,
               c.rca_deadline,
                c.rca1_deadline,
                c.rca2_deadline,
                c.lodged_by_agent,
                c.lodged_from_web,
                c.close_feedback
            FROM complaints c
            JOIN employees e ON c.reference_number = e.employee_id
            WHERE e.office_id = %s  AND c.status NOT IN ('Unapproved','Rejected');
        """
        cursor.execute(sql_query, (your_company_id,))
    complaints_data = cursor.fetchall()
    # Execute the query with the company ID as a parameter
    
    temp_complaint = list(complaints_data)
    for i in temp_complaint:
        if not i:
            i = ''
    complaint = temp_complaint
    # Convert the fetched complaints into a list of dictionaries
    fetched_complaints = []
    for complaint in complaints_data:
        office_name = None
        company_name = None
        designation  = ''
        gender = ''
        if complaint[13] == 'Closed':
            temp_complaint = list(complaint)
            temp_complaint[13] = 'Submitted'
            complaint = temp_complaint
        if complaint[4] == True:
            temp_complaint = list(complaint)
            temp_complaint[14] = 'Anonymous'
            temp_complaint[5] = 'N/A'
            temp_complaint[40] = ''
            complaint = temp_complaint

        cursor.execute(f"""SELECT company_id,office_name from offices WHERE office_id IN (
        SELECT office_id from employees WHERE employee_id = {complaint[2]})""")
        office_name = cursor.fetchone()

        cursor.execute(f"""SELECT name from companies WHERE company_id = {office_name[0]}""")
        office_name = office_name[1]
        company_name = cursor.fetchone()

        if company_name:
            company_name = company_name[0]
        else:
            company_name = None
        import datetime
        fetched_complaints.append({
            "ticket_number": complaint[1],
            "is_urgent": complaint[3],
            "is_anonymous": complaint[4],
            "mobile_number": complaint[5],
            "date_of_issue": complaint[6].strftime('%a, %d %b %Y') if isinstance(complaint[6], datetime.datetime) else complaint[6],
            "complaint_categories": complaint[7],
            "additional_comments": complaint[8],
            "person_issue": complaint[9],
            "concerned_department": complaint[10],
            "previous_history": complaint[11],
            "proposed_solution": complaint[12],
            "status": complaint[13],
            "employee_name": complaint[14],
            "date_entry": complaint[15].strftime('%a, %d %b %Y %I:%M:%S %p') if complaint[15] else None,
            "in_process_date": complaint[16].strftime('%a, %d %b %Y %I:%M:%S %p') if complaint[16] else None,
            "capa_date": complaint[17].strftime('%a, %d %b %Y %I:%M:%S %p') if complaint[17] else None,
            "rca_date": complaint[18].strftime('%a, %d %b %Y %I:%M:%S %p') if complaint[18] else None,
            "capa": complaint[19],
            "rca": complaint[20],
            "closed_date": complaint[21].strftime('%a, %d %b %Y %I:%M %p') if complaint[21] else None,
            "bounced_date": complaint[22].strftime('%a, %d %b %Y %I:%M %p') if complaint[22] else None,
            "capa1_date": complaint[23].strftime('%a, %d %b %Y %I:%M %p') if complaint[23] else None,
            "capa2_date": complaint[24].strftime('%a, %d %b %Y %I:%M %p') if complaint[24] else None,
            "capa3_date": complaint[25].strftime('%a, %d %b %Y %I:%M %p') if complaint[25] else None,
            "rca1_date": complaint[26].strftime('%a, %d %b %Y %I:%M %p') if complaint[26] else None,
            "rca2_date": complaint[27].strftime('%a, %d %b %Y %I:%M %p') if complaint[27] else None,
            "rca3_date": complaint[28].strftime('%a, %d %b %Y %I:%M %p') if complaint[28] else None,
            "bounced1_date": complaint[29].strftime('%a, %d %b %Y %I:%M %p') if complaint[29] else None,
            "bounced2_date": complaint[30].strftime('%a, %d %b %Y %I:%M %p') if complaint[30] else None,
            "bounced3_date": complaint[31].strftime('%a, %d %b %Y %I:%M %p') if complaint[31] else None,
            "capa1": complaint[32],
            "capa2": complaint[33],
            "capa3": complaint[34],
            "rca1": complaint[35],
            "rca2": complaint[36],
            "rca3": complaint[37],
            'office_name':office_name,
            'company_name':company_name,
            "completed_date": complaint[38].strftime('%a, %d %b %Y %I:%M %p') if complaint[38] else None,
            'gender':complaint[39],
            'designation':complaint[40],
            'feedback':complaint[41],
            'feedback1':complaint[42],
            'capa_deadline': complaint[43].strftime('%a, %d %b %Y %I:%M %p') if complaint[43] else None,
            'capa_deadline1': complaint[44].strftime('%a, %d %b %Y %I:%M %p') if complaint[44] else None,
            'capa_deadline2': complaint[45].strftime('%a, %d %b %Y %I:%M %p') if complaint[45] else None,
            'lodged_by_agent': complaint[46],
            'lodged_from_web': complaint[47],
            'closed_feedback': complaint[48]
        })
    cursor.close()
    conn.close()
    return fetched_complaints


def get_data_from_database_for_download(your_company_id, start_date, end_date):
    conn = get_retryable_connection('admin')
    cursor = conn.cursor()
    # SQL query to fetch office IDs from the database
    cursor.execute(f"""SELECT office_id FROM offices WHERE company_id IN 
    (SELECT company_id FROM buyer_company WHERE buyer_id = %s)""", (your_company_id,))
    office_ids = cursor.fetchall()
    
    regular_complaints = []
    feedback_complaints = []
    dormitory_complaints = []
    
    if office_ids:
        for office in office_ids:
            office_id = office[0]
            
            # Base SQL query
            if your_company_id in range(141,148):
                base_sql = """
                SELECT c.complaint_no,
                       c.ticket_number,
                       c.reference_number,
                       c.is_urgent,
                       1 as is_anonymous,
                       c.mobile_number AS complaint_mobile_number,
                       c.date_of_issue,
                       c.complaint_categories,
                       c.additional_comments,
                       c.person_issue,
                       c.concerned_department,
                       c.previous_history,
                       c.proposed_solution,
                       c.status,
                       e.employee_name,
                       c.date_entry,
                       c.in_process_date,
                       c.capa_date,
                       c.rca_date,
                       c.capa,
                       c.rca,
                       c.closed_date,
                       c.bounced_date,
                       c.capa1_date,
                       c.capa2_date,
                       c.capa3_date,
                       c.rca1_date,
                       c.rca2_date,
                       c.rca3_date,
                       c.bounced1_date,
                       c.bounced2_date,
                       c.bounced3_date,
                       c.capa1,
                       c.capa2,
                       c.capa3,
                       c.rca1,
                       c.rca2,
                       c.rca3,
                       c.completed_date,
                       e.gender,
                       e.designation,
                       c.feedback,
                       c.feedback1,
                       c.rca_deadline,
                       c.rca1_deadline,
                       c.rca2_deadline,
                       c.lodged_by_agent,
                       c.lodged_from_web,
                       c.close_feedback
                FROM complaints c
                JOIN employees e ON c.reference_number = e.employee_id
                WHERE e.office_id = %s 
                  AND c.status NOT IN ('Unapproved', 'Rejected')
                  AND c.date_entry BETWEEN %s AND %s
                """
            else:
                base_sql = """
                SELECT c.complaint_no,
                       c.ticket_number,
                       c.reference_number,
                       c.is_urgent,
                       c.is_anonymous,
                       c.mobile_number AS complaint_mobile_number,
                       c.date_of_issue,
                       c.complaint_categories,
                       c.additional_comments,
                       c.person_issue,
                       c.concerned_department,
                       c.previous_history,
                       c.proposed_solution,
                       c.status,
                       e.employee_name,
                       c.date_entry,
                       c.in_process_date,
                       c.capa_date,
                       c.rca_date,
                       c.capa,
                       c.rca,
                       c.closed_date,
                       c.bounced_date,
                       c.capa1_date,
                       c.capa2_date,
                       c.capa3_date,
                       c.rca1_date,
                       c.rca2_date,
                       c.rca3_date,
                       c.bounced1_date,
                       c.bounced2_date,
                       c.bounced3_date,
                       c.capa1,
                       c.capa2,
                       c.capa3,
                       c.rca1,
                       c.rca2,
                       c.rca3,
                       c.completed_date,
                       e.gender,
                       e.designation,
                       c.feedback,
                       c.feedback1,
                       c.rca_deadline,
                       c.rca1_deadline,
                       c.rca2_deadline,
                       c.lodged_by_agent,
                       c.lodged_from_web,
                       c.close_feedback
                FROM complaints c
                JOIN employees e ON c.reference_number = e.employee_id
                WHERE e.office_id = %s 
                  AND c.status NOT IN ('Unapproved', 'Rejected')
                  AND c.date_entry BETWEEN %s AND %s
                """
            
            # Query for regular complaints (no feedback status and no dormitory complaints)
            regular_sql = base_sql + " AND c.complaint_categories != 'Feedback' AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%'"
            
            # Query for feedback complaints
            feedback_sql = base_sql + " AND c.complaint_categories = 'Feedback'"
            
            # Query for dormitory complaints
            dormitory_sql = base_sql + " AND LOWER(c.additional_comments) LIKE '%dormitory complaint%'"

            # Execute queries and process results
            for sql_query, complaint_list in [
                (regular_sql, regular_complaints),
                (feedback_sql, feedback_complaints),
                (dormitory_sql, dormitory_complaints)
            ]:
                cursor.execute(sql_query, (office_id, start_date, end_date))
                complaints_data = cursor.fetchall()
                
                for complaint in complaints_data:
                    if complaint[4]:  # If anonymous
                        temp_complaint = list(complaint)
                        temp_complaint[14] = 'Anonymous'
                        temp_complaint[40] = ''
                        complaint = tuple(temp_complaint)
                    
                    cursor.execute("""SELECT company_id, office_name FROM offices 
                                    WHERE office_id IN (SELECT office_id FROM employees WHERE employee_id = %s)""", 
                                 (complaint[2],))
                    office_info = cursor.fetchone()
                    office_name = office_info[1]
                    
                    cursor.execute("""SELECT name FROM companies WHERE company_id = %s""", (office_info[0],))
                    company_name = cursor.fetchone()[0]
                    ticket_number = complaint[1]
                    if your_company_id in range(141,148):
                        # Modify the ticket number format
                        ticket_number = ticket_number[:11] + 'XXXX'
                                
                    complaint_dict = {
                        "ticket_number": ticket_number,
                        "complaint_categories": complaint[7],
                        "additional_comments": complaint[8],
                        "person_issue": complaint[9],
                        "concerned_department": complaint[10],
                        "previous_history": complaint[11],
                        "proposed_solution": complaint[12],
                        "date_entry": complaint[15].strftime('%a, %d %b %Y %I:%M %p') if complaint[15] else None,
                        "status": complaint[13],
                        "capa": complaint[19],
                        "rca": complaint[20],
                        "capa1": complaint[32],
                        "capa2": complaint[33],
                        "capa3": complaint[34],
                        "rca1": complaint[35],
                        "rca2": complaint[36],
                        "rca3": complaint[37],
                        "completed_date": complaint[38].strftime('%a, %d %b %Y %I:%M %p') if complaint[38] else None,
                        "feedback": complaint[41],
                        "feedback1": complaint[42],
                        "close_feedback": complaint[48],
                        "office_name": office_name,
                        "company_name": company_name
                    }
                    complaint_list.append(complaint_dict)
    
    cursor.close()
    conn.close()
    return regular_complaints, feedback_complaints, dormitory_complaints


def get_data_from_database_for_buyer(your_company_id):
    conn = get_retryable_connection('admin')
    cursor = conn.cursor()
    # SQL query to fetch data from the database
    cursor.execute(f"""SELECT office_id from offices where company_id IN 
    (SELECT company_id from buyer_company where buyer_id = {your_company_id})""")
    office_id = cursor.fetchall()
    fetched_complaints = []
    if office_id:
        for office in office_id:
            if your_company_id == 16:
                sql_query = """
                    SELECT c.complaint_no,
                       c.ticket_number,
                       c.reference_number,
                       c.is_urgent,
                       c.is_anonymous,
                       c.mobile_number AS complaint_mobile_number,
                       c.date_of_issue,
                       c.complaint_categories,
                       c.additional_comments,
                       c.person_issue,
                       c.concerned_department,
                       c.previous_history,
                       c.proposed_solution,
                       c.status,
                       e.employee_name,
                       c.date_entry,
                       c.in_process_date,
                       c.capa_date,
                       c.rca_date,
                       c.capa,
                       c.rca,
                       c.closed_date,
                       c.bounced_date,
                       c.capa1_date,
                       c.capa2_date,
                       c.capa3_date,
                       c.rca1_date,
                       c.rca2_date,
                       c.rca3_date,
                       c.bounced1_date,
                       c.bounced2_date,
                       c.bounced3_date,
                       c.capa1,
                       c.capa2,
                       c.capa3,
                       c.rca1,
                       c.rca2,
                       c.rca3,
                       c.completed_date,
                       e.gender,
                       e.designation,
                       c.feedback,
                       c.feedback1,
                       c.rca_deadline,
                       c.rca1_deadline,
                       c.rca2_deadline,
                       c.lodged_by_agent,
                       c.lodged_from_web,
                       c.close_feedback,
                       e.office_id
                    FROM complaints c
                    JOIN employees e ON c.reference_number = e.employee_id
                    WHERE e.office_id = %s AND c.status NOT IN ('Unapproved','Rejected') and c.enabled = 1 AND c.complaint_categories != 'Feedback' AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%';
                """
            elif your_company_id == 17:
                sql_query = """
                    SELECT c.complaint_no,
                       c.ticket_number,
                       c.reference_number,
                       c.is_urgent,
                       c.is_anonymous,
                       c.mobile_number AS complaint_mobile_number,
                       c.date_of_issue,
                       c.complaint_categories,
                       c.additional_comments,
                       c.person_issue,
                       c.concerned_department,
                       c.previous_history,
                       c.proposed_solution,
                       c.status,
                       e.employee_name,
                       c.date_entry,
                       c.in_process_date,
                       c.capa_date,
                       c.rca_date,
                       c.capa,
                       c.rca,
                       c.closed_date,
                       c.bounced_date,
                       c.capa1_date,
                       c.capa2_date,
                       c.capa3_date,
                       c.rca1_date,
                       c.rca2_date,
                       c.rca3_date,
                       c.bounced1_date,
                       c.bounced2_date,
                       c.bounced3_date,
                       c.capa1,
                       c.capa2,
                       c.capa3,
                       c.rca1,
                       c.rca2,
                       c.rca3,
                       c.completed_date,
                       e.gender,
                       e.designation,
                       c.feedback,
                       c.feedback1,
                       c.rca_deadline,
                       c.rca1_deadline,
                       c.rca2_deadline,
                       c.lodged_by_agent,
                       c.lodged_from_web,
                       c.close_feedback,
                       e.office_id
                    FROM complaints c
                    JOIN employees e ON c.reference_number = e.employee_id
                    WHERE e.office_id = %s AND c.status NOT IN ('Unapproved','Rejected') and c.enabled = 1 AND c.complaint_categories != 'Feedback' AND LOWER(c.additional_comments) LIKE '%dormitory complaint%';
                """
            elif your_company_id == 15:
                sql_query = """
                    SELECT c.complaint_no,
                       c.ticket_number,
                       c.reference_number,
                       c.is_urgent,
                       c.is_anonymous,
                       c.mobile_number AS complaint_mobile_number,
                       c.date_of_issue,
                       c.complaint_categories,
                       c.additional_comments,
                       c.person_issue,
                       c.concerned_department,
                       c.previous_history,
                       c.proposed_solution,
                       c.status,
                       e.employee_name,
                       c.date_entry,
                       c.in_process_date,
                       c.capa_date,
                       c.rca_date,
                       c.capa,
                       c.rca,
                       c.closed_date,
                       c.bounced_date,
                       c.capa1_date,
                       c.capa2_date,
                       c.capa3_date,
                       c.rca1_date,
                       c.rca2_date,
                       c.rca3_date,
                       c.bounced1_date,
                       c.bounced2_date,
                       c.bounced3_date,
                       c.capa1,
                       c.capa2,
                       c.capa3,
                       c.rca1,
                       c.rca2,
                       c.rca3,
                       c.completed_date,
                       e.gender,
                       e.designation,
                       c.feedback,
                       c.feedback1,
                       c.rca_deadline,
                       c.rca1_deadline,
                       c.rca2_deadline,
                       c.lodged_by_agent,
                       c.lodged_from_web,
                       c.close_feedback,
                       e.office_id
                    FROM complaints c
                    JOIN employees e ON c.reference_number = e.employee_id
                    WHERE e.office_id = %s AND c.status NOT IN ('Unapproved','Rejected') AND LOWER(c.additional_comments) NOT LIKE '%dormitory complaint%';
                """

            elif your_company_id == 128:
                sql_query = """
                    SELECT c.complaint_no,
                       c.ticket_number,
                       c.reference_number,
                       c.is_urgent,
                       c.is_anonymous,
                       c.mobile_number AS complaint_mobile_number,
                       c.date_of_issue,
                       c.complaint_categories,
                       c.additional_comments,
                       c.person_issue,
                       c.concerned_department,
                       c.previous_history,
                       c.proposed_solution,
                       c.status,
                       e.employee_name,
                       c.date_entry,
                       c.in_process_date,
                       c.capa_date,
                       c.rca_date,
                       c.capa,
                       c.rca,
                       c.closed_date,
                       c.bounced_date,
                       c.capa1_date,
                       c.capa2_date,
                       c.capa3_date,
                       c.rca1_date,
                       c.rca2_date,
                       c.rca3_date,
                       c.bounced1_date,
                       c.bounced2_date,
                       c.bounced3_date,
                       c.capa1,
                       c.capa2,
                       c.capa3,
                       c.rca1,
                       c.rca2,
                       c.rca3,
                       c.completed_date,
                       e.gender,
                       e.designation,
                       c.feedback,
                       c.feedback1,
                       c.rca_deadline,
                       c.rca1_deadline,
                       c.rca2_deadline,
                       c.lodged_by_agent,
                       c.lodged_from_web,
                       c.close_feedback,
                       e.office_id
                    FROM complaints c
                    JOIN employees e ON c.reference_number = e.employee_id
                    WHERE e.office_id = %s AND c.status NOT IN ('Unapproved','Rejected') and c.enabled = 1;
                """
            elif your_company_id in range(170,179):
                sql_query = """
                    SELECT c.complaint_no,
                       c.ticket_number,
                       c.reference_number,
                       c.is_urgent,
                       c.is_anonymous,
                       c.mobile_number AS complaint_mobile_number,
                       c.date_of_issue,
                       c.complaint_categories,
                       c.additional_comments,
                       c.person_issue,
                       c.concerned_department,
                       c.previous_history,
                       c.proposed_solution,
                       c.status,
                       e.employee_name,
                       c.date_entry,
                       c.in_process_date,
                       c.capa_date,
                       c.rca_date,
                       c.capa,
                       c.rca,
                       c.closed_date,
                       c.bounced_date,
                       c.capa1_date,
                       c.capa2_date,
                       c.capa3_date,
                       c.rca1_date,
                       c.rca2_date,
                       c.rca3_date,
                       c.bounced1_date,
                       c.bounced2_date,
                       c.bounced3_date,
                       c.capa1,
                       c.capa2,
                       c.capa3,
                       c.rca1,
                       c.rca2,
                       c.rca3,
                       c.completed_date,
                       e.gender,
                       e.designation,
                       c.feedback,
                       c.feedback1,
                       c.rca_deadline,
                       c.rca1_deadline,
                       c.rca2_deadline,
                       c.lodged_by_agent,
                       c.lodged_from_web,
                       c.close_feedback,
                       e.office_id
                    FROM complaints c
                    JOIN employees e ON c.reference_number = e.employee_id
                    WHERE e.office_id = %s AND c.status NOT IN ('Unapproved','Rejected') AND c.status = 'Completed';
                """
            elif your_company_id in range(141,148):
                sql_query = """
                    SELECT c.complaint_no,
                       c.ticket_number,
                       c.reference_number,
                       c.is_urgent,
                       1 as is_anonymous,
                       c.mobile_number AS complaint_mobile_number,
                       c.date_of_issue,
                       c.complaint_categories,
                       c.additional_comments,
                       c.person_issue,
                       c.concerned_department,
                       c.previous_history,
                       c.proposed_solution,
                       c.status,
                       e.employee_name,
                       c.date_entry,
                       c.in_process_date,
                       c.capa_date,
                       c.rca_date,
                       c.capa,
                       c.rca,
                       c.closed_date,
                       c.bounced_date,
                       c.capa1_date,
                       c.capa2_date,
                       c.capa3_date,
                       c.rca1_date,
                       c.rca2_date,
                       c.rca3_date,
                       c.bounced1_date,
                       c.bounced2_date,
                       c.bounced3_date,
                       c.capa1,
                       c.capa2,
                       c.capa3,
                       c.rca1,
                       c.rca2,
                       c.rca3,
                       c.completed_date,
                       e.gender,
                       e.designation,
                       c.feedback,
                       c.feedback1,
                       c.rca_deadline,
                       c.rca1_deadline,
                       c.rca2_deadline,
                       c.lodged_by_agent,
                       c.lodged_from_web,
                       c.close_feedback,
                       e.office_id
                    FROM complaints c
                    JOIN employees e ON c.reference_number = e.employee_id
                    WHERE e.office_id = %s AND c.status = 'Completed';
                """
            else:
                sql_query = """
                    SELECT c.complaint_no,
                       c.ticket_number,
                       c.reference_number,
                       c.is_urgent,
                       c.is_anonymous,
                       c.mobile_number AS complaint_mobile_number,
                       c.date_of_issue,
                       c.complaint_categories,
                       c.additional_comments,
                       c.person_issue,
                       c.concerned_department,
                       c.previous_history,
                       c.proposed_solution,
                       c.status,
                       e.employee_name,
                       c.date_entry,
                       c.in_process_date,
                       c.capa_date,
                       c.rca_date,
                       c.capa,
                       c.rca,
                       c.closed_date,
                       c.bounced_date,
                       c.capa1_date,
                       c.capa2_date,
                       c.capa3_date,
                       c.rca1_date,
                       c.rca2_date,
                       c.rca3_date,
                       c.bounced1_date,
                       c.bounced2_date,
                       c.bounced3_date,
                       c.capa1,
                       c.capa2,
                       c.capa3,
                       c.rca1,
                       c.rca2,
                       c.rca3,
                       c.completed_date,
                       e.gender,
                       e.designation,
                       c.feedback,
                       c.feedback1,
                       c.rca_deadline,
                       c.rca1_deadline,
                       c.rca2_deadline,
                       c.lodged_by_agent,
                       c.lodged_from_web,
                       c.close_feedback,
                       e.office_id
                    FROM complaints c
                    JOIN employees e ON c.reference_number = e.employee_id
                    WHERE e.office_id = %s AND c.status NOT IN ('Unapproved','Rejected');
                """

            # Execute the query with the company ID as a parameter
            cursor.execute(sql_query, (office[0],))

            # Fetch all the complaints
            complaints_data = cursor.fetchall()
            temp_complaint = list(complaints_data)
            for i in temp_complaint:
                if not i:
                    i = ''
            complaint = temp_complaint
            # Convert the fetched complaints into a list of dictionaries

            for complaint in complaints_data:
                office_name = None
                company_name = None
                designation = ''
                gender = ''
                if complaint[4] == True:
                    temp_complaint = list(complaint)
                    temp_complaint[14] = ''
                    temp_complaint[40] = ''
                    complaint = temp_complaint
                cursor.execute(f"""SELECT company_id,office_name from offices WHERE office_id IN (
                SELECT office_id from employees WHERE employee_id = {complaint[2]})""")
                office_name = cursor.fetchone()
                cursor.execute(f"""SELECT name from companies WHERE company_id = {office_name[0]}""")
                office_name = office_name[1]
                company_name = cursor.fetchone()[0]

                import datetime
                ticket_number = complaint[1]
                if your_company_id in range(141,148):
                    # Modify the ticket number format
                    ticket_number = ticket_number[:11] + 'XXXX'
                fetched_complaints.append({
                    "ticket_number": ticket_number,
                    "is_urgent": complaint[3],
                    "is_anonymous": complaint[4],
                    "mobile_number": complaint[5],
                    "date_of_issue": complaint[6].strftime('%a, %d %b %Y') if isinstance(complaint[6],
                                                                                         datetime.datetime) else
                    complaint[6],
                    "complaint_categories": complaint[7],
                    "additional_comments": complaint[8],
                    "person_issue": complaint[9],
                    "concerned_department": complaint[10],
                    "previous_history": complaint[11],
                    "proposed_solution": complaint[12],
                    "status": complaint[13],
                    "employee_name": complaint[14],
                    "date_entry": complaint[15].strftime('%a, %d %b %Y %I:%M %p') if complaint[15] else None,
                    "in_process_date": complaint[16].strftime('%a, %d %b %Y %I:%M %p') if complaint[16] else None,
                    "capa_date": complaint[17].strftime('%a, %d %b %Y %I:%M %p') if complaint[17] else None,
                    "rca_date": complaint[18].strftime('%a, %d %b %Y %I:%M %p') if complaint[18] else None,
                    "capa": complaint[19],
                    "rca": complaint[20],
                    "closed_date": complaint[21].strftime('%a, %d %b %Y %I:%M %p') if complaint[21] else None,
                    "bounced_date": complaint[22].strftime('%a, %d %b %Y %I:%M %p') if complaint[22] else None,
                    "capa1_date": complaint[23].strftime('%a, %d %b %Y %I:%M %p') if complaint[23] else None,
                    "capa2_date": complaint[24].strftime('%a, %d %b %Y %I:%M %p') if complaint[24] else None,
                    "capa3_date": complaint[25].strftime('%a, %d %b %Y %I:%M %p') if complaint[25] else None,
                    "rca1_date": complaint[26].strftime('%a, %d %b %Y %I:%M %p') if complaint[26] else None,
                    "rca2_date": complaint[27].strftime('%a, %d %b %Y %I:%M %p') if complaint[27] else None,
                    "rca3_date": complaint[28].strftime('%a, %d %b %Y %I:%M %p') if complaint[28] else None,
                    "bounced1_date": complaint[29].strftime('%a, %d %b %Y %I:%M %p') if complaint[29] else None,
                    "bounced2_date": complaint[30].strftime('%a, %d %b %Y %I:%M %p') if complaint[30] else None,
                    "bounced3_date": complaint[31].strftime('%a, %d %b %Y %I:%M %p') if complaint[31] else None,
                    "capa1": complaint[32],
                    "capa2": complaint[33],
                    "capa3": complaint[34],
                    "rca1": complaint[35],
                    "rca2": complaint[36],
                    "rca3": complaint[37],
                    'office_name': office_name,
                    'company_name': company_name,
                    "completed_date": complaint[38].strftime('%a, %d %b %Y %I:%M %p') if complaint[38] else None,
                    'gender': complaint[39],
                    'designation': complaint[40],
                    'feedback': complaint[41],
                    'feedback1': complaint[42],
                    'capa_deadline': complaint[43].strftime('%a, %d %b %Y %I:%M %p') if complaint[43] else None,
                    'capa_deadline1': complaint[44].strftime('%a, %d %b %Y %I:%M %p') if complaint[44] else None,
                    'capa_deadline2': complaint[45].strftime('%a, %d %b %Y %I:%M %p') if complaint[45] else None,
                    'lodged_by_agent': complaint[46],
                    'lodged_from_web': complaint[47],
                    'closed_feedback': complaint[48],
                    'office_id': complaint[49]
                })
    cursor.close()
    conn.close()
    return fetched_complaints

def get_data_of_unregistered_complaints():
    # SQL query to fetch data from the database
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    sql_query = """
        SELECT c.complaint_no,
         c.ticket_number,
              c.reference_number,
              c.is_urgent,
              c.is_anonymous,
              c.mobile_number AS complaint_mobile_number,
              c.date_of_issue,
              c.complaint_categories,
              c.additional_comments,
              c.person_issue,
              c.concerned_department,
              c.previous_history,
              c.proposed_solution,
              c.status,
              c.date_entry,
              c.in_process_date,
              c.capa_date,
              c.rca_date,
              c.capa,
              c.rca,
              c.closed_date,
              c.bounced_date,
              c.capa1_date,
              c.capa2_date,
              c.capa3_date,
              c.rca1_date,
              c.rca2_date,
              c.rca3_date,
              c.bounced1_date,
              c.bounced2_date,
              c.bounced3_date,
              c.capa1,
              c.capa2,
              c.capa3,
              c.rca1,
              c.rca2,
              c.rca3,
              c.completed_date,
              c.feedback,
              c.feedback1
    FROM complaints c
    WHERE c.reference_number IS NULL;
    """

    # Execute the query with the company ID as a parameter
    cursor.execute(sql_query,)

    # Fetch all the complaints
    complaints_data = cursor.fetchall()
    temp_complaint = list(complaints_data)
    for i in temp_complaint:
        if not i:
            i = ''
    complaint = temp_complaint
    # Convert the fetched complaints into a list of dictionaries
    fetched_complaints = []
    for complaint in complaints_data:
        office_name = None
        company_name = None
        gender = None
        if complaint[13] == 'Closed':
            temp_complaint = list(complaint)
            temp_complaint[13] = 'Submitted'
            complaint = temp_complaint
        if complaint[4] == True:
            temp_complaint = list(complaint)
            temp_complaint[14] = ''
            complaint = temp_complaint
        import datetime
        fetched_complaints.append({
            "ticket_number": complaint[1],
            "is_urgent": complaint[3],
            "is_anonymous": complaint[4],
            "mobile_number": complaint[5],
            "date_of_issue": complaint[6].strftime('%a, %d %b %Y') if isinstance(complaint[6], datetime.datetime) else
            complaint[6],
            "complaint_categories": complaint[7],
            "additional_comments": complaint[8],
            "person_issue": complaint[9],
            "concerned_department": complaint[10],
            "previous_history": complaint[11],
            "proposed_solution": complaint[12],
            "status": complaint[13],
            "employee_name": '',
            "date_entry": complaint[14].strftime('%a, %d %b %Y %I:%M %p') if complaint[15] else None,
            "in_process_date": complaint[15].strftime('%a, %d %b %Y %I:%M %p') if complaint[16] else None,
            "capa_date": complaint[16].strftime('%a, %d %b %Y %I:%M %p') if complaint[17] else None,
            "rca_date": complaint[17].strftime('%a, %d %b %Y %I:%M %p') if complaint[18] else None,
            "capa": complaint[18],
            "rca": complaint[19],
            "closed_date": complaint[20].strftime('%a, %d %b %Y %I:%M %p') if complaint[21] else None,
            "bounced_date": complaint[21].strftime('%a, %d %b %Y %I:%M %p') if complaint[22] else None,
            "capa1_date": complaint[22].strftime('%a, %d %b %Y %I:%M %p') if complaint[23] else None,
            "capa2_date": complaint[23].strftime('%a, %d %b %Y %I:%M %p') if complaint[24] else None,
            "capa3_date": complaint[24].strftime('%a, %d %b %Y %I:%M %p') if complaint[25] else None,
            "rca1_date": complaint[25].strftime('%a, %d %b %Y %I:%M %p') if complaint[26] else None,
            "rca2_date": complaint[26].strftime('%a, %d %b %Y %I:%M %p') if complaint[27] else None,
            "rca3_date": complaint[27].strftime('%a, %d %b %Y %I:%M %p') if complaint[28] else None,
            "bounced1_date": complaint[28].strftime('%a, %d %b %Y %I:%M %p') if complaint[29] else None,
            "bounced2_date": complaint[29].strftime('%a, %d %b %Y %I:%M %p') if complaint[30] else None,
            "bounced3_date": complaint[30].strftime('%a, %d %b %Y %I:%M %p') if complaint[31] else None,
            "capa1": complaint[31],
            "capa2": complaint[32],
            "capa3": complaint[33],
            "rca1": complaint[34],
            "rca2": complaint[35],
            "rca3": complaint[36],
            'office_name': '',
            'company_name': '',
            "completed_date": complaint[37].strftime('%a, %d %b %Y %I:%M %p') if complaint[38] else None,
            'gender': '',
            'designation': '',
            'feedback': complaint[38],
            'feedback1': complaint[39]
        })
    cursor.close()
    conn.close()
    return fetched_complaints
    
    
def get_data_from_database_for_cs():
    # SQL query to fetch data from the database
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    sql_query = """
        SELECT c.complaint_no,
          c.ticket_number,
                   c.reference_number,
                   c.is_urgent,
                   c.is_anonymous,
                   c.mobile_number AS complaint_mobile_number,
                   c.date_of_issue,
                   c.complaint_categories,
                   c.additional_comments,
                   c.person_issue,
                   c.concerned_department,
                   c.previous_history,
                   c.proposed_solution,
                   c.status,
                   e.employee_name,
                   c.date_entry,
                   c.in_process_date,
                   c.capa_date,
                   c.rca_date,
                   c.capa,
                   c.rca,
                   c.closed_date,
                   c.bounced_date,
                   c.capa1_date,
                   c.capa2_date,
                   c.capa3_date,
                   c.rca1_date,
                   c.rca2_date,
                   c.rca3_date,
                   c.bounced1_date,
                   c.bounced2_date,
                   c.bounced3_date,
                   c.capa1,
                   c.capa2,
                   c.capa3,
                   c.rca1,
                   c.rca2,
                   c.rca3,
                   c.completed_date,
                   e.gender,
                   e.designation,
                   c.feedback,
                   c.feedback1,
                   c.rca_deadline,
                   c.rca1_deadline,
                   c.rca2_deadline,
                   c.lodged_by_agent,
                   c.lodged_from_web,
                    c.close_feedback
        FROM complaints c
        JOIN employees e ON c.reference_number = e.employee_id;
    """

    # Execute the query with the company ID as a parameter
    cursor.execute(sql_query,)

    # Fetch all the complaints
    complaints_data = cursor.fetchall()
    temp_complaint = list(complaints_data)
    for i in temp_complaint:
        if not i:
            i = ''
    complaint = temp_complaint
    # Convert the fetched complaints into a list of dictionaries
    fetched_complaints = []
    for complaint in complaints_data:
        office_name = None
        company_name = None
        gender = None
        if complaint[13] == 'Closed':
            temp_complaint = list(complaint)
            temp_complaint[13] = 'Submitted'
            complaint = temp_complaint
        

        cursor.execute(f"""SELECT company_id,office_name,office_id from offices WHERE office_id IN (
        SELECT office_id from employees WHERE employee_id = {complaint[2]})""")
        office_name = cursor.fetchone()
        office_id = office_name[2]
        cursor.execute(f"""SELECT name from companies WHERE company_id = {office_name[0]}""")
        office_name = office_name[1]
        company_name = cursor.fetchone()[0]
        cursor.execute(f"""SELECT gender from employees WHERE employee_id={complaint[2]}""")
        gender = cursor.fetchone()[0]
        import datetime
        fetched_complaints.append({
            "ticket_number": complaint[1],
            'employee_id': complaint[2],
            "is_urgent": complaint[3],
            "is_anonymous": complaint[4],
            "mobile_number": complaint[5],
            "date_of_issue": complaint[6].strftime('%a, %d %b %Y') if isinstance(complaint[6], datetime.datetime) else
            complaint[6],
            "complaint_categories": complaint[7],
            "additional_comments": complaint[8],
            "person_issue": complaint[9],
            "concerned_department": complaint[10],
            "previous_history": complaint[11],
            "proposed_solution": complaint[12],
            "status": complaint[13],
            "employee_name": complaint[14],
            "date_entry": complaint[15].strftime('%a, %d %b %Y %I:%M %p') if complaint[15] else None,
            "in_process_date": complaint[16].strftime('%a, %d %b %Y %I:%M %p') if complaint[16] else None,
            "capa_date": complaint[17].strftime('%a, %d %b %Y %I:%M %p') if complaint[17] else None,
            "rca_date": complaint[18].strftime('%a, %d %b %Y %I:%M %p') if complaint[18] else None,
            "capa": complaint[19],
            "rca": complaint[20],
            "closed_date": complaint[21].strftime('%a, %d %b %Y %I:%M %p') if complaint[21] else None,
            "bounced_date": complaint[22].strftime('%a, %d %b %Y %I:%M %p') if complaint[22] else None,
            "capa1_date": complaint[23].strftime('%a, %d %b %Y %I:%M %p') if complaint[23] else None,
            "capa2_date": complaint[24].strftime('%a, %d %b %Y %I:%M %p') if complaint[24] else None,
            "capa3_date": complaint[25].strftime('%a, %d %b %Y %I:%M %p') if complaint[25] else None,
            "rca1_date": complaint[26].strftime('%a, %d %b %Y %I:%M %p') if complaint[26] else None,
            "rca2_date": complaint[27].strftime('%a, %d %b %Y %I:%M %p') if complaint[27] else None,
            "rca3_date": complaint[28].strftime('%a, %d %b %Y %I:%M %p') if complaint[28] else None,
            "bounced1_date": complaint[29].strftime('%a, %d %b %Y %I:%M %p') if complaint[29] else None,
            "bounced2_date": complaint[30].strftime('%a, %d %b %Y %I:%M %p') if complaint[30] else None,
            "bounced3_date": complaint[31].strftime('%a, %d %b %Y %I:%M %p') if complaint[31] else None,
            "capa1": complaint[32],
            "capa2": complaint[33],
            "capa3": complaint[34],
            "rca1": complaint[35],
            "rca2": complaint[36],
            "rca3": complaint[37],
            'office_name': office_name,
            'company_name': company_name,
            "completed_date": complaint[38].strftime('%a, %d %b %Y %I:%M %p') if complaint[38] else None,
            'gender': complaint[39],
            'designation': complaint[40],
            'feedback': complaint[41],
            'feedback1': complaint[42],
            'capa_deadline': complaint[43].strftime('%a, %d %b %Y %I:%M %p') if complaint[43] else None,
            'capa_deadline1': complaint[44].strftime('%a, %d %b %Y %I:%M %p') if complaint[44] else None,
            'capa_deadline2': complaint[45].strftime('%a, %d %b %Y %I:%M %p') if complaint[45] else None,
            'lodged_by_agent': complaint[46],
            'lodged_from_web': complaint[47],
            'office_id': office_id,
            'closed_feedback': complaint[48]
            
        })
    cursor.close()
    conn.close()
    return fetched_complaints

def get_employee_data():
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    dictionary = {}
    for row in rows:
        id = row[0]
        name = row[1]
        worker_type = row[2]
        department = row[3]
        designation = row[4]
        mobile_number = row[5]
        gender = row[6]
        company_name = row[7]
        dictionary[id] = {
            "name": name,
            "worker_type": worker_type,
            "department": department,
            "designation": designation,
            "mobile_number": mobile_number,
            "gender": gender,
            "company_name": company_name
        }
    cursor.close()
    conn.close()
    return dictionary


from datetime import datetime, timedelta

def calculate_working_hours(start_time, end_time):
    # Define the Pakistani timezone
    pakistani_tz = pytz.timezone('Asia/Karachi')
    
    # If either of the dates are naive, localize them to Pakistani timezone
    if start_time.tzinfo is None or start_time.tzinfo.utcoffset(start_time) is None:
        start_time = pakistani_tz.localize(start_time)
    if end_time.tzinfo is None or end_time.tzinfo.utcoffset(end_time) is None:
        end_time = pakistani_tz.localize(end_time)
    
    workday_start = datetime.strptime("09:00:00", "%H:%M:%S").time()
    workday_end = datetime.strptime("17:00:00", "%H:%M:%S").time()
    workdays = [0, 1, 2, 3, 4]  # Monday to Friday

    total_working_hours = 0

    current_time = start_time
    if start_time and end_time:
        while current_time < end_time:
            if current_time.weekday() in workdays:
                start_of_day = datetime.combine(current_time.date(), workday_start).astimezone(pakistani_tz)
                end_of_day = datetime.combine(current_time.date(), workday_end).astimezone(pakistani_tz)
                work_period_start = max(current_time, start_of_day)
                work_period_end = min(end_time, end_of_day)
                if work_period_start < work_period_end:
                    total_working_hours += (work_period_end - work_period_start).total_seconds() / 3600
            current_time += timedelta(days=1)
            current_time = datetime.combine(current_time.date(), workday_start).astimezone(pakistani_tz)  # Start from the beginning of the next workday

        return total_working_hours
    return 0





def complaints_resolution_time_percentage(office_id):
    # Define the Pakistani timezone
    pakistani_tz = pytz.timezone('Asia/Karachi')

    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    cursor.execute(f"""
            SELECT
                date_entry,
                capa_date,
                in_process_date,
                capa1_date,
                bounced_date,
                capa2_date,
                bounced1_date,
                is_urgent
            FROM
                complaints WHERE reference_number in 
                (SELECT employee_id from employees where office_id={office_id});
        """)

    result = cursor.fetchall()

    result_dict = {}
    current_date = datetime.now().astimezone(pakistani_tz)  # Adjust current date to Pakistani timezone
    date_ranges = {
        '30 days': (current_date - timedelta(days=30), current_date),
        '90 days': (current_date - timedelta(days=90), current_date),
        '180 days': (current_date - timedelta(days=180), current_date),
        '360 days': (current_date - timedelta(days=360), current_date)
    }

    for complaints_count_entry in result:
        # Convert each datetime to Pakistani timezone
        entry_date = complaints_count_entry[0].astimezone(pakistani_tz) if complaints_count_entry[0] else None
        capa_date = complaints_count_entry[1].astimezone(pakistani_tz) if complaints_count_entry[1] else None
        in_process_date = complaints_count_entry[2].astimezone(pakistani_tz) if complaints_count_entry[2] else None
        capa1_date = complaints_count_entry[3].astimezone(pakistani_tz) if complaints_count_entry[3] else None
        bounced_date = complaints_count_entry[4].astimezone(pakistani_tz) if complaints_count_entry[4] else None
        capa2_date = complaints_count_entry[5].astimezone(pakistani_tz) if complaints_count_entry[5] else None
        bounced1_date = complaints_count_entry[6].astimezone(pakistani_tz) if complaints_count_entry[6] else None

        total_resolution_time = 0

        # Calculate differences and add to total_resolution_time
        for start_date, end_date in [(in_process_date, capa_date), (bounced_date, capa1_date),
                                     (bounced1_date, capa2_date)]:
            if start_date and end_date:
                total_resolution_time += calculate_working_hours(start_date, end_date)

        if complaints_count_entry[7] == 1:
            total_resolution_time /= 7.5
        else:
            total_resolution_time /= 10

        for period_name, date_range in date_ranges.items():
            start_date, end_date = date_range
            if start_date <= entry_date <= end_date:
                if period_name not in result_dict:
                    result_dict[period_name] = []
                result_dict[period_name].append(total_resolution_time)

    final_result = {}
    for period_name, res_list in result_dict.items():
        late_time = sum(res for res in res_list if res > 1)
        total_time = sum(res_list)
        if total_time > 0:
            final_result[period_name] = round(late_time / total_time, 3)
        else:
            final_result[period_name] = 0
    cursor.close()
    conn.close()
    return final_result

def complaints_resolution_time_percentage_for_safety(office_id):
    # Define the Pakistani timezone
    pakistani_tz = pytz.timezone('Asia/Karachi')

    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT
            date_entry,
            capa_date,
            in_process_date,
            capa1_date,
            bounced_date,
            capa2_date,
            bounced1_date,
            is_urgent
        FROM
            complaints WHERE complaint_categories = 'Workplace Health, Safety and Environment' and reference_number in 
            (SELECT employee_id from employees where office_id={office_id});
    """)

    result = cursor.fetchall()

    result_dict = {}
    current_date = datetime.now().astimezone(pakistani_tz)  # Adjust current date to Pakistani timezone
    date_ranges = {
        '30 days': (current_date - timedelta(days=30), current_date),
        '90 days': (current_date - timedelta(days=90), current_date),
        '180 days': (current_date - timedelta(days=180), current_date),
        '360 days': (current_date - timedelta(days=360), current_date)
    }

    for complaints_count_entry in result:
        # Convert each datetime to Pakistani timezone
        entry_date = complaints_count_entry[0].astimezone(pakistani_tz) if complaints_count_entry[0] else None
        capa_date = complaints_count_entry[1].astimezone(pakistani_tz) if complaints_count_entry[1] else None
        in_process_date = complaints_count_entry[2].astimezone(pakistani_tz) if complaints_count_entry[2] else None
        capa1_date = complaints_count_entry[3].astimezone(pakistani_tz) if complaints_count_entry[3] else None
        bounced_date = complaints_count_entry[4].astimezone(pakistani_tz) if complaints_count_entry[4] else None
        capa2_date = complaints_count_entry[5].astimezone(pakistani_tz) if complaints_count_entry[5] else None
        bounced1_date = complaints_count_entry[6].astimezone(pakistani_tz) if complaints_count_entry[6] else None

        total_resolution_time = 0

        # Calculate differences and add to total_resolution_time
        for start_date, end_date in [(in_process_date, capa_date), (bounced_date, capa1_date),
                                     (bounced1_date, capa2_date)]:
            if start_date and end_date:
                total_resolution_time += calculate_working_hours(start_date, end_date)

        if complaints_count_entry[7] == 1:
            total_resolution_time /= 7.5
        else:
            total_resolution_time /= 10

        for period_name, date_range in date_ranges.items():
            start_date, end_date = date_range
            if start_date <= entry_date <= end_date:
                if period_name not in result_dict:
                    result_dict[period_name] = []
                result_dict[period_name].append(total_resolution_time)

    final_result = {}
    for period_name, res_list in result_dict.items():
        late_time = sum(res for res in res_list if res > 1)
        total_time = sum(res_list)
        if total_time > 0:
            final_result[period_name] = round(late_time / total_time, 3)
        else:
            final_result[period_name] = 0
    cursor.close()
    conn.close()
    return final_result



def get_complaints_response_time(office_id):
    # Define the Pakistani timezone
    pakistani_tz = pytz.timezone('Asia/Karachi')

    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    cursor.execute(f"""
                SELECT
                    DATE_FORMAT(date_entry, '%Y') AS year,
                    MONTHNAME(date_entry) AS month_name,
                    in_process_date,date_entry
                FROM
                    complaints WHERE reference_number in 
                    (SELECT employee_id from employees where office_id={office_id});
                """)
    result = cursor.fetchall()

    result_dict = {}
    current_date = datetime.now().astimezone(pakistani_tz)  # Adjust current date to Pakistani timezone
    date_ranges = {
        '30 days': (current_date - timedelta(days=30), current_date),
        '90 days': (current_date - timedelta(days=90), current_date),
        '180 days': (current_date - timedelta(days=180), current_date),
        '360 days': (current_date - timedelta(days=360), current_date)
    }

    for complaints_count_entry in result:
        # Convert each datetime to Pakistani timezone
        entry_date = complaints_count_entry[3].astimezone(pakistani_tz) if complaints_count_entry[3] else None
        in_process_date = complaints_count_entry[2].astimezone(pakistani_tz) if complaints_count_entry[2] else None

        total_resolution_time = 0

        # Calculate differences and add to total_resolution_time
        if entry_date and in_process_date:
            total_resolution_time += calculate_working_hours(entry_date, in_process_date)

        if total_resolution_time:
            total_resolution_time /= 2

        for period_name, date_range in date_ranges.items():
            start_date, end_date = date_range
            if start_date <= entry_date <= end_date:
                if period_name not in result_dict:
                    result_dict[period_name] = []
                result_dict[period_name].append(total_resolution_time)

    final_result = {}
    for period_name, res_list in result_dict.items():
        late_time = sum(res for res in res_list if res > 1)
        total_time = sum(res_list)
        if total_time > 0:
            final_result[period_name] = round(late_time / total_time, 3)
        else:
            final_result[period_name] = 0
    cursor.close()
    conn.close()
    return final_result

def get_bounced_percentage_without_weightage(office_id):
    # Define the Pakistani timezone
    pakistani_tz = pytz.timezone('Asia/Karachi')

    conn = get_retryable_connection('user-admin1')
    cursor = conn.cursor()
    current_datetime_pakistani = datetime.now(pakistani_tz)  # Get current date and time in Pakistani timezone

    date_ranges = {
        '30 days': (current_datetime_pakistani - timedelta(days=30), current_datetime_pakistani),
        '90 days': (current_datetime_pakistani - timedelta(days=90), current_datetime_pakistani),
        '180 days': (current_datetime_pakistani - timedelta(days=180), current_datetime_pakistani),
        '360 days': (current_datetime_pakistani - timedelta(days=360), current_datetime_pakistani)
    }

    query = f"""
            SELECT 
                bounced_date,
                bounced1_date,
                complaint_categories
            FROM complaints 
            WHERE 
                DATE(CONVERT_TZ(date_entry, 'UTC', 'Asia/Karachi')) BETWEEN %s AND %s 
                AND reference_number IN (
                    SELECT employee_id FROM employees WHERE office_id = {office_id}
                )
        """

    # Initialize dictionaries for bounced count and total count
    bounced_count = {}
    total_count = {}

    # Execute the query and process results for each date range
    for range_name, (start_date, end_date) in date_ranges.items():
        # Convert date ranges to Pakistani timezone
        start_date_pakistani = start_date.astimezone(pakistani_tz)
        end_date_pakistani = end_date.astimezone(pakistani_tz)

        cursor.execute(
            query,
            (start_date_pakistani.strftime('%Y-%m-%d %H:%M:%S'), end_date_pakistani.strftime('%Y-%m-%d %H:%M:%S'))
        )
        results = cursor.fetchall()

        bounced_count[range_name] = 0
        total_count[range_name] = 0

        for row in results:
            weightage = 1

            if row[1]:
                weightage *= 3
            elif row[0]:
                weightage *= 1
            else:
                weightage = 0

            bounced_count[range_name] += weightage
            total_count[range_name] += 1

    # Calculate the bounced rate for each time period
    bounced_rate_dict = {}
    for range_name in date_ranges.keys():
        if total_count[range_name] > 0:
            bounced_rate_dict[range_name] = round(bounced_count[range_name] / total_count[range_name], 2)
        else:
            bounced_rate_dict[range_name] = 0
    cursor.close()
    conn.close()
    return bounced_rate_dict
def calculate_io_performance(office_id):
    response_time = get_complaints_response_time(office_id)
    resolution_time = complaints_resolution_time_percentage(office_id)
    bounced_rate = get_bounced_percentage_without_weightage(office_id)
    result_dict = {}
    if response_time:

        for period, value in response_time.items():
            try:
                resolution_value = resolution_time[period]
            except:
                resolution_value = 0
            try:
                bounced_value = bounced_rate[period]
            except:
                bounced_value = 0

            result_dict[period] = ((value * 0.2) + (resolution_value * 0.3) + (bounced_value * 0.5)) * 100

        return result_dict
    return {}
def get_bounced_percentage_with_weightage(office_id):
    # Define the Pakistani timezone
    pakistani_tz = pytz.timezone('Asia/Karachi')

    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    current_datetime_pakistani = datetime.now(pakistani_tz)  # Get current date and time in Pakistani timezone

    date_ranges = {
        '30 days': (current_datetime_pakistani - timedelta(days=30), current_datetime_pakistani),
        '90 days': (current_datetime_pakistani - timedelta(days=90), current_datetime_pakistani),
        '180 days': (current_datetime_pakistani - timedelta(days=180), current_datetime_pakistani),
        '360 days': (current_datetime_pakistani - timedelta(days=360), current_datetime_pakistani)
    }

    category_weightage = {
        "Harassment": 1.4,
        "Unfair Employment": 1.5,
        "Child Labor": 1.6,
        "Forced Labor": 1.7,
        "Discrimination": 1.8,
        "Ethical Business": 1.9,
        "Freedom of Association": 2,
        "Wages & Benefits": 2.1,
        "Working Hours": 2.2,
        "Workplace Health, Safety and Environment": 2.3,
        'Workplace Discipline': 1.4,
        'Feedback': 1
    }

    query = f"""
        SELECT 
            bounced_date,
            bounced1_date,
            complaint_categories
        FROM complaints 
        WHERE 
            DATE(CONVERT_TZ(date_entry, 'UTC', 'Asia/Karachi')) BETWEEN %s AND %s 
            AND reference_number IN (
                SELECT employee_id FROM employees WHERE office_id = {office_id}
            )
    """

    # Initialize dictionaries for bounced count and total count
    bounced_count = {}
    total_count = {}

    # Execute the query and process results for each date range
    for range_name, (start_date, end_date) in date_ranges.items():
        # Convert date ranges to Pakistani timezone
        start_date_pakistani = start_date.astimezone(pakistani_tz)
        end_date_pakistani = end_date.astimezone(pakistani_tz)

        cursor.execute(
            query,
            (start_date_pakistani.strftime('%Y-%m-%d %H:%M:%S'), end_date_pakistani.strftime('%Y-%m-%d %H:%M:%S'))
        )
        results = cursor.fetchall()

        bounced_count[range_name] = 0
        total_count[range_name] = 0

        for row in results:
            weightage = category_weightage.get(row[2], 1)

            if row[1]:
                weightage *= 3
            elif row[0]:
                weightage *= 1
            else:
                weightage = 0

            bounced_count[range_name] += weightage
            total_count[range_name] += 1

    # Calculate the bounced rate for each time period
    bounced_rate_dict = {}
    for range_name in date_ranges.keys():
        if total_count[range_name] > 0:
            bounced_rate_dict[range_name] = round(bounced_count[range_name] / total_count[range_name], 2)
        else:
            bounced_rate_dict[range_name] = 0

    cursor.close()
    conn.close()

    return bounced_rate_dict


def get_bounced_percentage_with_weightage_for_safety(office_id):
    # Define the Pakistani timezone
    pakistani_tz = pytz.timezone('Asia/Karachi')

    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    category_weightage = {
        "Harassment": 1.4,
        "Unfair Employment": 1.5,
        "Child Labor": 1.6,
        "Forced Labor": 1.7,
        "Discrimination": 1.8,
        "Ethical Business": 1.9,
        "Freedom of Association": 2,
        "Wages & Benefits": 2.1,
        "Working Hours": 2.2,
        "Workplace Health, Safety and Environment": 2.3,
        'Workplace Discipline': 1.4,
        'Feedback': 1
    }

    # Calculate the date ranges using Pakistani timezone
    current_datetime_pakistani = datetime.now(pakistani_tz)
    date_ranges = {
        '30 days': (current_datetime_pakistani - timedelta(days=30), current_datetime_pakistani),
        '90 days': (current_datetime_pakistani - timedelta(days=90), current_datetime_pakistani),
        '180 days': (current_datetime_pakistani - timedelta(days=180), current_datetime_pakistani),
        '360 days': (current_datetime_pakistani - timedelta(days=360), current_datetime_pakistani)
    }

    # Construct the SQL query
    query = f"""
        SELECT 
            DATE_FORMAT(CONVERT_TZ(date_entry, 'UTC', 'Asia/Karachi'), '%Y') AS year,
            MONTHNAME(CONVERT_TZ(date_entry, 'UTC', 'Asia/Karachi')) AS month_name,
            bounced_date,
            bounced1_date
        FROM complaints 
        WHERE 
            DATE(CONVERT_TZ(date_entry, 'UTC', 'Asia/Karachi')) BETWEEN %s AND %s 
            AND complaint_categories = 'Workplace Health, Safety and Environment'
            AND reference_number IN (SELECT employee_id FROM employees WHERE office_id = {office_id})
    """

    # Initialize dictionaries for bounced count and total count
    bounced_count = {}
    total_count = {}

    # Execute the query and process results for each date range
    for range_name, (start_date, end_date) in date_ranges.items():
        start_date_pakistani = start_date.astimezone(pakistani_tz)
        end_date_pakistani = end_date.astimezone(pakistani_tz)

        cursor.execute(
            query,
            (start_date_pakistani.strftime('%Y-%m-%d %H:%M:%S'), end_date_pakistani.strftime('%Y-%m-%d %H:%M:%S'))
        )
        results = cursor.fetchall()

        bounced_count[range_name] = 0
        total_count[range_name] = 0

        for row in results:
            weightage = category_weightage.get("Workplace Health, Safety and Environment", 2)

            if row[1]:
                weightage *= 3
            elif row[0]:
                weightage *= 1
            else:
                weightage = 0

            bounced_count[range_name] += weightage
            total_count[range_name] += 1

    # Calculate the bounced rate for each time period
    bounced_rate_dict = {}
    for range_name in date_ranges.keys():
        if total_count[range_name] > 0:
            bounced_rate_dict[range_name] = round(bounced_count[range_name] / total_count[range_name], 2)
            if bounced_rate_dict[range_name] > 1:
                bounced_rate_dict[range_name] = 1
        else:
            bounced_rate_dict[range_name] = 0

    cursor.close()
    conn.close()

    return bounced_rate_dict



def complaints_over_employees(office_id):
    def calculate_period(start_date, end_date):
        conn = get_retryable_connection('personal')
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COUNT(*) as complaint_count
            FROM complaints 
            WHERE reference_number IN (SELECT employee_id FROM employees WHERE office_id = {office_id})
                AND date_entry BETWEEN %s AND %s
        """, (start_date, end_date))
        complaint_count = cursor.fetchone()[0]

        cursor.execute(f"""SELECT COUNT(*) FROM employees WHERE office_id = {office_id}""")
        total_employees = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        if total_employees > 0:
            return round(complaint_count / total_employees, 2)
        else:
            return 0

    # Initialize the all_periods_data dictionary
    all_periods_data = {}

    # Calculate the date ranges
    current_date = datetime.now()
    date_ranges = {
        '30 days': (current_date - timedelta(days=30), current_date),
        '90 days': (current_date - timedelta(days=90), current_date),
        '180 days': (current_date - timedelta(days=180), current_date),
        '360 days': (current_date - timedelta(days=360), current_date)
    }

    # Calculate the complaints per employee for each period and store in the all_periods_data dictionary
    for range_name, (start_date, end_date) in date_ranges.items():
        period_data = calculate_period(start_date, end_date)
        if period_data >1:
            all_periods_data[range_name] = 1
        else:
            all_periods_data[range_name] = period_data

    # Return the all_periods_data dictionary
    return all_periods_data

def safety_complaints_over_total(office_id):
    def calculate_period(start_date, end_date, category):
        conn = get_retryable_connection('personal')
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT 
                COUNT(*) as complaint_count
            FROM complaints 
            WHERE complaint_categories = %s AND reference_number IN (SELECT employee_id FROM employees WHERE office_id = {office_id})
                AND date_entry BETWEEN %s AND %s
        """, (category, start_date, end_date))

        complaint_count = cursor.fetchone()[0]

        cursor.execute(
            f"""SELECT COUNT(*) FROM complaints WHERE reference_number IN (SELECT employee_id FROM employees WHERE office_id = {office_id})""")
        total_complaints = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        if total_complaints > 0:
            return round(complaint_count / total_complaints, 2)
        else:
            return 0

    # Initialize the all_periods_data dictionary
    all_periods_data = {}

    # Calculate the date ranges
    current_date = datetime.now()
    date_ranges = {
        '30 days': (current_date - timedelta(days=30), current_date),
        '90 days': (current_date - timedelta(days=90), current_date),
        '180 days': (current_date - timedelta(days=180), current_date),
        '360 days': (current_date - timedelta(days=360), current_date)
    }

    # Calculate the metrics for each period and store in the all_periods_data dictionary
    for range_name, (start_date, end_date) in date_ranges.items():
        period_value = calculate_period(start_date, end_date, 'Workplace Health, Safety and Environment')
        all_periods_data[range_name] = period_value

    # Return the all_periods_data dictionary
    return all_periods_data


def calculate_ess(office_id):
    bounced_percentage = get_bounced_percentage_with_weightage_for_safety(office_id)
    resolution_time = complaints_resolution_time_percentage_for_safety(office_id)
    complaint_employees = safety_complaints_over_total(office_id)


    result_dict = {}

    if complaint_employees:
        for period, value in complaint_employees.items():
                try:
                    resolution_value = resolution_time[period]
                except KeyError:
                    resolution_value = 0
                try:
                    bounced_value = bounced_percentage[period]
                except KeyError:
                    bounced_value = 0

                period_data =100- ((bounced_value * 0.2) + (resolution_value * 0.3) + (value * 0.5)) * 100
                result_dict[period] = period_data

    return result_dict


def calculate_ehs(office_id):
    bounced_percentage = get_bounced_percentage_with_weightage(office_id)
    resolution_time = complaints_resolution_time_percentage(office_id)
    complaint_employees = complaints_over_employees(office_id)
    result_dict = {}

    if complaint_employees:
        for period, value in complaint_employees.items():
            try:
                resolution_value = resolution_time[period]
            except KeyError:
                resolution_value = 0
            try:
                bounced_value = bounced_percentage[period]
            except KeyError:
                bounced_value = 0
            period_data = 100-((bounced_value * 0.2) + (resolution_value * 0.3) + (value * 0.5))*100
            result_dict[period] = round(period_data,2)

    return result_dict
def filter_last_30_days(dataframe, days_count):
    pakistani_tz = pytz.timezone('Asia/Karachi')
    
    dataframe['date_entry'] = pd.to_datetime(dataframe['date_entry'])
    now = pd.to_datetime(datetime.now(pakistani_tz))
    last_30_days = now - timedelta(days=days_count)
    
    # Ensure both sides of comparison are in datetime64 format
    filtered_dataframe = dataframe[(dataframe['date_entry'] >= last_30_days) | dataframe['date_entry'].isnull()]
    return filtered_dataframe

def filter_date_range(dataframe, start_date, end_date):
    pakistani_tz = pytz.timezone('Asia/Karachi')
    
    # Ensure the dataframe's date_entry column is in datetime64 format and timezone-aware
    dataframe['date_entry'] = pd.to_datetime(dataframe['date_entry']).dt.tz_localize(pakistani_tz, ambiguous='NaT', nonexistent='NaT')
    
    # Ensure both start_date and end_date are in pandas Timestamp format and timezone-aware
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    
    # Convert start_date and end_date to the desired timezone if they are timezone-aware
    if start_date.tzinfo is None:
        start_date = start_date.tz_localize(pakistani_tz)
    else:
        start_date = start_date.tz_convert(pakistani_tz)
    
    if end_date.tzinfo is None:
        end_date = end_date.tz_localize(pakistani_tz)
    else:
        end_date = end_date.tz_convert(pakistani_tz)
    
    print('Start:', start_date, 'End:', end_date)
    
    filtered_dataframe = dataframe[(dataframe['date_entry'] >= start_date) & (dataframe['date_entry'] <= end_date)]
    return filtered_dataframe
def get_dashboard_data_for_zero_complaint(buyer_id,final_dict):
    from datetime import datetime
    conn = get_retryable_connection('admin')
    cursor = conn.cursor()
    pakistani_tz = pytz.timezone('Asia/Karachi')
    sql_query = """
                SELECT *
                FROM offices
                LEFT JOIN companies ON offices.company_id = companies.company_id
                LEFT JOIN buyer_company ON companies.company_id = buyer_company.company_id
                LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
                WHERE buyers.buyer_id = %s;
            """
    cursor.execute(sql_query, (buyer_id,))
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    df = df.loc[:, ~df.columns.duplicated(keep='last')]
    sql_query = """
                    SELECT *
                    FROM employees WHERE office_id IN(SELECT office_id from offices where
                    company_id in (SELECT company_id from companies where company_id in 
                    (SELECT company_id from buyer_company where buyer_id = %s)));
                """
    cursor.execute(sql_query, (buyer_id,))
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    employees_df = pd.DataFrame(data, columns=columns)
    cursor.close()
    conn.close()
    total_emplyees_count = len(employees_df[employees_df['employee_left'] == False])
    grouped_df = df.groupby('office_id')
    offices_list = []
    for office_id, df in grouped_df:
        company_name = df['name'].iloc[0]
        if company_name in final_dict and any(d.get('office_id') == office_id for d in final_dict[company_name]) :
            continue
        else:
            final_result = {}
            final_result['office_name'] = df.loc[df['office_id'] == office_id, 'office_name'].iloc[0]
            final_result['office_id'] =  office_id
            employee_count = len(employees_df[employees_df['office_id'] == office_id])
            employee_count_without_leavers = len(employees_df[(employees_df['office_id'] == office_id) & (employees_df['employee_left'] == False)])
            final_result['total_employee'] = employee_count_without_leavers
            final_result['total_employees_overall'] = total_emplyees_count
            if company_name in final_dict:
                    final_dict[company_name].append(final_result)
            else:
                    final_dict[company_name] = [final_result]
    return final_dict
def get_data_for_dashboard(buyer_id, start_date, end_date):
    from datetime import datetime
    import pandas as pd
    import numpy as np
    import pytz

    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    conn = get_retryable_connection('admin')
    cursor = conn.cursor()
    pakistani_tz = pytz.timezone('Asia/Karachi')
    if buyer_id == 16:
        sql_query = """
            SELECT *
            FROM complaints
            LEFT JOIN employees ON complaints.reference_number = employees.employee_id
            RIGHT JOIN offices ON employees.office_id = offices.office_id
            LEFT JOIN companies ON offices.company_id = companies.company_id
            LEFT JOIN buyer_company ON companies.company_id = buyer_company.company_id
            LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
            WHERE buyers.buyer_id = %s AND complaints.status NOT IN ('Unapproved','Rejected') AND complaints.enabled = 1 AND complaints.complaint_categories != 'Feedback' AND LOWER(complaints.additional_comments) NOT LIKE '%dormitory complaint%';
        """
    elif buyer_id == 17:
        sql_query = """
            SELECT *
            FROM complaints
            LEFT JOIN employees ON complaints.reference_number = employees.employee_id
            RIGHT JOIN offices ON employees.office_id = offices.office_id
            LEFT JOIN companies ON offices.company_id = companies.company_id
            LEFT JOIN buyer_company ON companies.company_id = buyer_company.company_id
            LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
            WHERE buyers.buyer_id = %s AND complaints.status NOT IN ('Unapproved','Rejected') AND complaints.enabled = 1 AND complaints.complaint_categories != 'Feedback' AND LOWER(complaints.additional_comments) LIKE '%dormitory complaint%';
        """
    elif buyer_id == 128:
        sql_query = """
            SELECT *
            FROM complaints
            LEFT JOIN employees ON complaints.reference_number = employees.employee_id
            RIGHT JOIN offices ON employees.office_id = offices.office_id
            LEFT JOIN companies ON offices.company_id = companies.company_id
            LEFT JOIN buyer_company ON companies.company_id = buyer_company.company_id
            LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
            WHERE buyers.buyer_id = %s AND complaints.status NOT IN ('Unapproved','Rejected') AND complaints.enabled = 1 AND complaints.complaint_categories != 'Feedback';
        """
    elif buyer_id in range(170,179):
        sql_query = """
            SELECT *
            FROM complaints
            LEFT JOIN employees ON complaints.reference_number = employees.employee_id
            RIGHT JOIN offices ON employees.office_id = offices.office_id
            LEFT JOIN companies ON offices.company_id = companies.company_id
            LEFT JOIN buyer_company ON companies.company_id = buyer_company.company_id
            LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
            WHERE buyers.buyer_id = %s AND complaints.status NOT IN ('Unapproved','Rejected') AND complaints.complaint_categories != 'Feedback' AND complaints.status = 'Completed';
        """
    elif buyer_id in range(141,148):
        sql_query = """
            SELECT complaints.*,1 as is_anonymous,employees.*,offices.*,companies.*,buyer_company.*,buyers.*
            FROM complaints
            LEFT JOIN employees ON complaints.reference_number = employees.employee_id
            RIGHT JOIN offices ON employees.office_id = offices.office_id
            LEFT JOIN companies ON offices.company_id = companies.company_id
            LEFT JOIN buyer_company ON companies.company_id = buyer_company.company_id
            LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
            WHERE buyers.buyer_id = %s AND complaints.status = 'Completed' AND complaints.complaint_categories != 'Feedback';
        """
    elif buyer_id == 15:
        sql_query = """
            SELECT *
            FROM complaints
            LEFT JOIN employees ON complaints.reference_number = employees.employee_id
            RIGHT JOIN offices ON employees.office_id = offices.office_id
            LEFT JOIN companies ON offices.company_id = companies.company_id
            LEFT JOIN buyer_company ON companies.company_id = buyer_company.company_id
            LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
            WHERE buyers.buyer_id = %s AND complaints.status NOT IN ('Unapproved','Rejected') AND complaints.complaint_categories != 'Feedback' AND LOWER(complaints.additional_comments) NOT LIKE '%dormitory complaint%';
        """
    else:
        sql_query = """
            SELECT *
            FROM complaints
            LEFT JOIN employees ON complaints.reference_number = employees.employee_id
            RIGHT JOIN offices ON employees.office_id = offices.office_id
            LEFT JOIN companies ON offices.company_id = companies.company_id
            LEFT JOIN buyer_company ON companies.company_id = buyer_company.company_id
            LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
            WHERE buyers.buyer_id = %s AND complaints.status NOT IN ('Unapproved','Rejected') AND complaints.complaint_categories != 'Feedback';
        """

    cursor.execute(sql_query, (buyer_id,))
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    allTimeComplaints = len(df['complaint_no'])
    df = df.loc[:, ~df.columns.duplicated(keep='last')]

    sql_query = """
        SELECT *
        FROM employees WHERE office_id IN(SELECT office_id from offices where
        company_id in (SELECT company_id from companies where company_id in 
        (SELECT company_id from buyer_company where buyer_id = %s)));
    """
    cursor.execute(sql_query, (buyer_id,))
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    employees_df = pd.DataFrame(data, columns=columns)
    cursor.close()
    conn.close()

    df = filter_date_range(df, start_date, end_date)
    final_dict = {}
    total_emplyees_count = len(employees_df[employees_df['employee_left'] == False])
    grouped_df = df.groupby('office_id')
    print('DF:', df)
    print('Buyer Id :', buyer_id)
    for office_id, df in grouped_df:
        company_name = df['name'].iloc[0]
        final_result = {}
        final_result['office_name'] = df.loc[df['office_id'] == office_id, 'office_name'].iloc[0]
        final_result['office_id'] = office_id
        df = df.dropna(subset=['ticket_number'])

        value_counts = df['status'].value_counts().to_dict()
        final_result['status_counts'] = value_counts

        gender_category_counts = df.groupby(['complaint_categories', 'gender']).size().unstack(fill_value=0)
        gender_category_dict = gender_category_counts.to_dict(orient='index')
        for category, counts in gender_category_dict.items():
            gender_category_dict[category] = [counts.get('Male', 0), counts.get('Female', 0)]
        final_result['gender_count'] = gender_category_dict

        complaint_category_counts = df['complaint_categories'].value_counts().to_dict()
        final_result['category_counts'] = complaint_category_counts

        df['date_entry'] = pd.to_datetime(df['date_entry'])
        pk_time = datetime.now(pakistani_tz)

        complaints_last_30_days = df[(df['date_entry'] >= start_date) & (df['date_entry'] <= end_date)].copy()
        complaints_last_30_days.sort_values(by='date_entry', inplace=True)

        daily_complaint_count = complaints_last_30_days['date_entry'].dt.date.value_counts().sort_index()
        all_dates = pd.date_range(start_date, periods=(end_date - start_date).days, freq='D').date
        daily_complaint_count = daily_complaint_count.reindex(all_dates, fill_value=0)
        complaint_count_list = daily_complaint_count.tolist()
        final_result['category_counts_by_days'] = complaint_count_list
        
        date_columns = ['in_process_date', 'capa_date', 'capa1_date']
        df[date_columns] = df[date_columns].apply(pd.to_datetime, errors='coerce')

        # Combine 'capa_date' and 'capa1_date' to get the final CAPA date
        df['final_capa_date'] = df['capa_date'].combine_first(df['capa1_date'])

        # Calculate the total resolution time, initially including all durations
        df['total_resolution_time'] = (df['final_capa_date'] - df['in_process_date']).dt.total_seconds() / 3600  # In hours
        df['closed_date'] = pd.to_datetime(df['closed_date'], errors='coerce')
        df['completed_date'] = pd.to_datetime(df['completed_date'], errors='coerce')

        # Calculate the duration of the interview (closed_date to completed_date)
        df['interview_time'] = np.where(
            (df['closed_date'].notnull()) & (df['completed_date'].notnull()),
            (df['completed_date'] - df['closed_date']).dt.total_seconds() / 3600,
            0  # If either date is missing, set interview time to 0
        )

        # Subtract the interview time from the total resolution time to get the actual resolution time
        df['resolution_time'] = df['total_resolution_time'] - df['interview_time']

        # Filter out invalid resolution times (negative or extremely large values)
        df['resolution_time'] = df['resolution_time'].clip(lower=0, upper=365*10)  # Assume max 10 years
        # Calculate statistics
        total_resolution_time = df['resolution_time'].sum()
        average_resolution_time = df['resolution_time'].mean()
        
        # Store results
        final_result['resolution_time'] = 0 if np.isnan(total_resolution_time) else total_resolution_time
        final_result['average_resolution_time'] = 0 if np.isnan(average_resolution_time) else average_resolution_time

        final_result['total_complaints_handled'] = len(complaints_last_30_days['complaint_no'])
        bounced1_count = len(complaints_last_30_days[complaints_last_30_days['bounced_date'].notnull()])
        bounced2_count = len(complaints_last_30_days[complaints_last_30_days['bounced1_date'].notnull()])
        final_result['bounce1_count'] = bounced1_count
        final_result['bounce2_count'] = bounced2_count
        df['date_entry'] = pd.to_datetime(df['date_entry']).dt.tz_localize(None)
        df['in_process_date'] = pd.to_datetime(df['in_process_date']).dt.tz_localize(None)
        
        in_processed_complaints = df[df['in_process_date'].notnull()]
        response_times = (in_processed_complaints['in_process_date'] - in_processed_complaints['date_entry']).dt.total_seconds() / 3600
        df['response_time'] = response_times
        response_times = df['response_time'].replace([np.inf, -np.inf], np.nan)
        final_result['response_time'] = response_times.sum()
        average_response_time = response_times.mean()
        final_result['average_response_time'] = average_response_time if not np.isnan(average_response_time) else 0
        
        final_result['total_complaints_resolved'] = len(df['complaint_no'])

        count_bounced_rows = len(df[(df['bounced_date'].notnull()) | (df['bounced1_date'].notnull()) | (df['bounced2_date'].notnull())])
        final_result['total_complaints_bounced'] = count_bounced_rows

        # Enhanced category_weightage
        category_weightage = {
            "Child Labor": 2.0,           # Most severe
            "Forced Labor": 1.9,
            "Discrimination": 1.8,
            "Harassment": 1.7,
            "Workplace Health, Safety and Environment": 1.6,
            "Wages & Benefits": 1.5,
            "Working Hours": 1.4,
            "Freedom of Association": 1.3,
            "Unfair Employment": 1.2,
            "Workplace Discipline": 1.1,
            "Ethical Business": 1.0,
            "Feedback": 0.5               # Least severe
        }

        df['bounced_per_with_weightage'] = (
            np.where(df['bounced1_date'].notna(), df['complaint_categories'].map(category_weightage) * 3,
            np.where((df['bounced_date'].notna()) & (df['bounced1_date'].isna()), df['complaint_categories'].map(category_weightage) * 1, 0))
        )
        bounced_per_with_weightage = df['bounced_per_with_weightage'].sum() / final_result['total_complaints_handled'] if final_result['total_complaints_handled'] != 0 else 0
        df['is_urgent'].replace(0, 0.75, inplace=True)
        df['resolution_time'] = (df['resolution_time']) / (df['is_urgent'] * 10)

        employee_count = len(employees_df[employees_df['office_id'] == office_id])
        employee_count_without_leavers = len(employees_df[(employees_df['office_id'] == office_id) & (employees_df['employee_left'] == False)])
        final_result['total_employee'] = employee_count_without_leavers
        final_result['total_employees_overall'] = total_emplyees_count

        complaints_over_employees = min(final_result['total_complaints_handled'] / employee_count if employee_count != 0 else 0, 1)

        resolution_time_per = df[df['resolution_time'] > 1]['resolution_time'].sum() / df['resolution_time'].sum() if df['resolution_time'].sum() != 0 else 0

        # Enhanced EHS Value calculation
        ehs_raw_score = 1 - (
            (bounced_per_with_weightage * 0.3) +  # Increased weight for bounced complaints
            (resolution_time_per * 0.4) +         # Increased weight for resolution time
            (complaints_over_employees * 0.3)     # Slightly reduced weight for complaint ratio
        )
        non_safety_complaints = df[df['complaint_categories'] != 'Workplace Health, Safety and Environment']

        # Calculate bounced_per_with_weightage
        bounced_complaints = non_safety_complaints[
            (non_safety_complaints['bounced_date'].notna()) | 
            (non_safety_complaints['bounced1_date'].notna()) | 
            (non_safety_complaints['bounced2_date'].notna())
        ]
        bounced_per_with_weightage = len(bounced_complaints) / len(non_safety_complaints) if len(non_safety_complaints) > 0 else 0

        # Calculate average resolution time for non-safety complaints
        non_safety_completed = non_safety_complaints[non_safety_complaints['completed_date'].notnull()]
        resolution_time_per = non_safety_completed['resolution_time'].mean() if len(non_safety_completed) > 0 else 0
        non_safety_responded = non_safety_complaints[non_safety_complaints['in_process_date'].notnull()]
        response_time_non_safety = (non_safety_responded['in_process_date'] - non_safety_responded['date_entry']).dt.total_seconds() / 3600
        avg_response_time_non_safety = response_time_non_safety.mean() if len(response_time_non_safety) > 0 else 0

        # Calculate complaints over employees (excluding safety complaints)
        complaints_over_employees = len(non_safety_complaints) / employee_count_without_leavers if employee_count_without_leavers > 0 else 0

        final_result['bounced_per_with_weightage'] = bounced_per_with_weightage
        final_result['resolution_time_per'] = resolution_time_per
        final_result['complaints_over_employees'] = round(complaints_over_employees,2)

        # Calculate average resolution time for non-safety complaints
        final_result['avg_response_time_non_safety'] = avg_response_time_non_safety

        
        ehs_raw_score = max(0, min(1, ehs_raw_score))  # Ensure the score is between 0 and 1
        if buyer_id == 99:
            final_result['ehs_value'] = 60 + (ehs_raw_score * 40)  # Scales the value between 80 and 100
        else:
            final_result['ehs_value'] = 60 + (ehs_raw_score * 40)  # Scales the value between 80 and 100


        resolution_time_per = df[df['resolution_time'] < 1]['resolution_time'].sum() / df['resolution_time'].sum() if df['resolution_time'].sum() != 0 else 1
        response_time_per = df[df['response_time'] < 1]['response_time'].sum() / df['response_time'].sum() if df['response_time'].sum() != 0 else 1

        df['is_bounced'] = np.where(df['bounced1_date'].notna(), 3,
                                    np.where((df['bounced_date'].notna()) & (df['bounced1_date'].isna()), 1, 0))

        bounced_over_complaints = df['is_bounced'].sum() / len(df[df['is_bounced'] > 0]) if len(df[df['is_bounced'] > 0]) != 0 else 1
        final_result['performance'] = ((response_time_per * 0.2) + (resolution_time_per * 0.3) + (bounced_over_complaints * 0.5)) * 100

        safety_complaints = df.loc[df['complaint_categories'] == 'Workplace Health, Safety and Environment']
        total_safety_complaints = len(safety_complaints)
        bounced_safety_complaints = safety_complaints['is_bounced'].sum()
        severely_bounced_safety_complaints = safety_complaints.loc[safety_complaints['is_bounced'] > 1, 'is_bounced'].sum()

        bounced_per_for_safety = bounced_safety_complaints / total_safety_complaints if total_safety_complaints != 0 else 0
        sum_is_bounced_for_safety = severely_bounced_safety_complaints / bounced_safety_complaints if bounced_safety_complaints != 0 else 0
        safety_complaints_over_total = total_safety_complaints / final_result['total_complaints_handled'] if final_result['total_complaints_handled'] != 0 else 0
        
        # Enhanced ESS Value calculation
        ess_raw_score = 1 - (
            (bounced_per_for_safety * 0.4) +           # Increased weight for bounced safety complaints
            (sum_is_bounced_for_safety * 0.4) +        # Increased weight for severely bounced safety complaints
            (safety_complaints_over_total * 0.2)       # Reduced weight for safety complaints ratio
        )
        safety_complaints = df[df['complaint_categories'] == 'Workplace Health, Safety and Environment']

        # Calculate bounced_per_for_safety
        bounced_safety_complaints = safety_complaints[
            (safety_complaints['bounced_date'].notna()) | 
            (safety_complaints['bounced1_date'].notna()) | 
            (safety_complaints['bounced2_date'].notna())
        ]
        bounced_per_for_safety = len(bounced_safety_complaints) / len(safety_complaints) if len(safety_complaints) > 0 else 0

        # Calculate average resolution time for safety complaints
        safety_completed = safety_complaints[safety_complaints['completed_date'].notnull()]
        resolution_time_per_safety = safety_completed['resolution_time'].mean() if len(safety_completed) > 0 else 0
        safety_responded = safety_complaints[safety_complaints['in_process_date'].notnull()]
        response_time_safety = (safety_responded['in_process_date'] - safety_responded['date_entry']).dt.total_seconds() / 3600
        avg_response_time_safety = response_time_safety.mean() if len(response_time_safety) > 0 else 0
        # Calculate safety complaints over total complaints
        safety_complaints_over_total = len(safety_complaints) / len(df) if len(df) > 0 else 0

        # Calculate safety complaints over employees
        safety_complaints_over_employees = len(safety_complaints) / employee_count_without_leavers if employee_count_without_leavers > 0 else 0

        final_result['bounced_per_for_safety'] = bounced_per_for_safety
        final_result['resolution_time_per_safety'] = resolution_time_per_safety
        final_result['safety_complaints_over_total'] = safety_complaints_over_total
        final_result['safety_complaints_over_employees'] = round(safety_complaints_over_employees,2)
        final_result['avg_response_time_safety'] = avg_response_time_safety
        ess_raw_score = max(0, min(1, ess_raw_score))  # Ensure the score is between 0 and 1
        if buyer_id == 99:
            final_result['ess_value'] = 60 + (ess_raw_score * 40)  # Scales the value between 80 and 100
        else:
            final_result['ess_value'] = 60 + (ess_raw_score * 40)  # Scales the value between 80 and 100

        if company_name in final_dict:
            final_dict[company_name].append(final_result)
        else:
            final_dict[company_name] = [final_result]

    final_dict = get_dashboard_data_for_zero_complaint(buyer_id, final_dict)
    return final_dict, allTimeComplaints
    

    
def get_department_names1(buyer_id):
    conn = get_retryable_connection('admin')
    cursor = conn.cursor()
    # SQL query to retrieve data from the "buyers_company" table
    pakistani_tz = pytz.timezone('Asia/Karachi')

    sql_query = """
        SELECT company_id FROM buyer_company WHERE buyer_id = %s
    """

    # Execute the SQL query with the provided buyer_id as a parameter
    cursor.execute(sql_query, (buyer_id,))
    # Fetch the result
    company_ids = cursor.fetchall()
    company_ids = [company_id[0] for company_id in company_ids]


    query = f"""
            SELECT o.office_id, o.office_name, c.name
            FROM offices o
            INNER JOIN companies c ON o.company_id = c.company_id
            WHERE o.company_id IN ({', '.join(map(str, company_ids))})
        """
    cursor.execute(query)

    # Fetch all the results into a list of tuples
    offices = cursor.fetchall()
    data = {}
    q_data = {}
    for office in offices:
        company_name = office[2]
        office_data = {
            'office_id': office[0],
            'office_name': office[1],
            'performance':55
        }
        # Query to get the complaint status count for each office
        office_id = office[0]



        current_date = datetime.now(pakistani_tz)
        date_ranges = {
            '30 days': (current_date - timedelta(days=30), current_date),
            '90 days': (current_date - timedelta(days=90), current_date),
            '180 days': (current_date - timedelta(days=180), current_date),
            '360 days': (current_date - timedelta(days=360), current_date)
        }
        status_query = f"""
            SELECT status, COUNT(*) AS count
            FROM complaints
            WHERE status IN ('Unprocessed', 'In Process', 'Bounced', 'Closed', 'Bounced1', 'Bounced2', 'Unclosed')
              AND reference_number IN (
                  SELECT employee_id FROM employees WHERE office_id = {office_id}
              )
              AND date_entry BETWEEN %s AND %s
            GROUP BY status
        """

        final_result = {}

        # Execute the query and process results for each date range
        for range_name, (start_date, end_date) in date_ranges.items():
            cursor.execute(status_query, (start_date, end_date))
            status_counts = cursor.fetchall()

            status_count_dict = {}
            possible_statuses = ['Unprocessed', 'In Process', 'Bounced', 'Closed', 'Bounced1', 'Bounced2', 'Unclosed']

            for row in status_counts:
                status = row[0]
                count = row[1]
                status_count_dict[status] = count

            range_data = {status: status_count_dict.get(status, 0) for status in possible_statuses}
            final_result[range_name] = range_data

        # Add the final_result to office_data
        office_data['status_counts'] = final_result

        query = f"""
            SELECT
                c.complaint_categories,
                CAST(SUM(CASE WHEN e.gender = 'Male' THEN 1 ELSE 0 END) AS SIGNED) AS male_count,
                CAST(SUM(CASE WHEN e.gender = 'Female' THEN 1 ELSE 0 END) AS SIGNED) AS female_count
            FROM
                complaints c
            JOIN
                employees e ON c.reference_number = e.employee_id
            WHERE
                c.complaint_categories IN (
                    'Workplace Health, Safety and Environment',
                    'Freedom of Association',
                    'Child Labor',
                    'Wages & Benefits',
                    'Working Hours',
                    'Forced Labor',
                    'Discrimination',
                    'Unfair Employment',
                    'Ethical Business',
                    'Harassment',
                    'Workplace Discipline',
                    'Feedback'
                )
                AND e.office_id = {office_id}
                AND c.date_entry BETWEEN %s AND %s
            GROUP BY
                c.complaint_categories;
        """

        final_result = {}

        # Execute the query and process results for each date range
        for range_name, (start_date, end_date) in date_ranges.items():
            cursor.execute(query, (start_date, end_date))
            gender_count = cursor.fetchall()

            gender_count_dict = {}

            for gender in gender_count:
                category = gender[0]
                male_count = gender[1]
                female_count = gender[2]
                gender_count_dict[category] = [male_count, female_count]

            final_result[range_name] = gender_count_dict

        # Add the final_result to office_data
        office_data['gender_count'] = final_result
        # Calculate quarterly data by summing up monthly data
        office_quarterly_data = {}

        category_query = f"""
            SELECT
                c.complaint_categories,
                COUNT(*) AS count
            FROM
                complaints c
            JOIN
                employees e ON c.reference_number = e.employee_id
            WHERE
                c.complaint_categories IN (
                    'Workplace Health, Safety and Environment',
                    'Freedom of Association',
                    'Child Labor',
                    'Wages & Benefits',
                    'Working Hours',
                    'Forced Labor',
                    'Discrimination',
                    'Unfair Employment',
                    'Ethical Business',
                    'Harassment',
                    'Workplace Discipline',
                    'Feedback'
                )
                AND e.office_id = {office_id}
                AND c.date_entry BETWEEN %s AND %s
            GROUP BY
                c.complaint_categories;
        """

        final_result = {}

        # Execute the query and process results for each date range
        for range_name, (start_date, end_date) in date_ranges.items():
            cursor.execute(category_query, (start_date, end_date))
            category_counts = cursor.fetchall()

            category_count_dict = {}

            for category in category_counts:
                category_name = category[0]
                count = category[1]
                category_count_dict[category_name] = count

            final_result[range_name] = category_count_dict

        # Add the final_result to office_data
        office_data['category_counts'] = final_result
        query = f"""SELECT date_entry FROM complaints where reference_number in
        ( select employee_id from employees where office_id ={office_id})"""
        cursor.execute(query)
        complaints_data = [row[0] for row in cursor.fetchall()]

        # Create a dictionary to store the results
        complaints_by_time_period = {}

        # Loop through the date ranges and count complaints for each range
        for period, (start_date, end_date) in date_ranges.items():
            complaints_count = []
            for day in range((end_date - start_date).days + 1):
                date_to_check = start_date + timedelta(days=day)
                complaints_on_day = len([date for date in complaints_data if date.date() == date_to_check.date()])
                complaints_count.append(complaints_on_day)

            complaints_by_time_period[period] = complaints_count

        office_data['category_counts_by_days']  = complaints_by_time_period
        cursor.execute(f"""SElECT count(*) from employees where office_id = {office_id}""")
        total_employees = cursor.fetchone()[0]
        office_data['total_employee'] = total_employees

        query = f"""
            SELECT
                DATE_FORMAT(date_entry, '%Y') AS year,
                DATE_FORMAT(date_entry, '%m') AS month_number,
                MONTHNAME(date_entry) AS month_name,
                capa_date,
                in_process_date,
                capa1_date,
                bounced_date,
                capa2_date,
                bounced1_date,
                status
            FROM
                complaints
            WHERE
                reference_number IN (SELECT employee_id FROM employees WHERE office_id = {office_id});
        """

        cursor.execute(query)
        result = cursor.fetchall()

        final_result = {}

        for range_name, (start_date, end_date) in date_ranges.items():
            total_resolution_time = 0
            total_complaints = 0
            for complaints_count_entry in result:
                entry_year = complaints_count_entry[0]
                entry_month_name = complaints_count_entry[2]
                capa_date = complaints_count_entry[3]
                in_process_date = complaints_count_entry[4]
                capa1_date = complaints_count_entry[5]
                bounced_date = complaints_count_entry[6]
                capa2_date = complaints_count_entry[7]
                bounced1_date = complaints_count_entry[8]
                status = complaints_count_entry[9]

                entry_date = datetime.strptime(f"{entry_year}-{entry_month_name}", "%Y-%B")
                entry_date = pakistani_tz.localize(entry_date)
                if start_date <= entry_date <= end_date:
                    if status != 'Unprocessed' and status!='In Process':
                        total_complaints += 1

                    # Calculate differences and add to total_resolution_time
                    for start, end in [(in_process_date, capa_date), (bounced_date, capa1_date),
                                       (bounced1_date, capa2_date)]:
                        if start and end:
                            total_resolution_time += calculate_working_hours(start, end)

            if total_complaints > 0:
                average_resolution_time = total_resolution_time / total_complaints
            else:
                average_resolution_time = 0

            final_result[range_name] = average_resolution_time

        office_data['average_resolution_time'] = final_result
        query = f"""
            SELECT
                COUNT(*) AS number_of_complaints
            FROM
                complaints
            WHERE
                reference_number IN (
                    SELECT employee_id FROM employees WHERE office_id = {office_data['office_id']}
                )
                AND date_entry BETWEEN %s AND %s;
        """

        final_result = {}

        # Execute the query and process results for each date range
        for range_name, (start_date, end_date) in date_ranges.items():
            cursor.execute(query, (start_date, end_date))
            complaints_count_data = cursor.fetchone()

            if complaints_count_data:
                complaints_count = complaints_count_data[0]
            else:
                complaints_count = 0

            final_result[range_name] = complaints_count

        # Add the final_result to office_data
        office_data['total_complaints_handled'] = final_result

        office_id = office_data['office_id']
        query = f"""
            SELECT
                DATE_FORMAT(date_entry, '%Y') AS year,
                MONTHNAME(date_entry) AS month_name,
                in_process_date, date_entry, status
            FROM
                complaints
            WHERE
                reference_number IN (
                    SELECT employee_id FROM employees WHERE office_id = {office_id}
                );
        """

        cursor.execute(query)
        result = cursor.fetchall()
        
        final_result = {}
        
        for range_name, (start_date, end_date) in date_ranges.items():
            # Convert date_ranges to Karachi timezone (assuming they are naive to begin with)
            
            total_response_time = 0
            total_complaints = 0
        
            for complaints_count_entry in result:
                year = complaints_count_entry[0]
                month_name = complaints_count_entry[1]
                date_entry = complaints_count_entry[3]
                in_process_date = complaints_count_entry[2]
                status = complaints_count_entry[4]
        
                entry_date = datetime.strptime(f"{year}-{month_name}", "%Y-%B")
                entry_date = pakistani_tz.localize(entry_date)
        
                # Ensure all dates are in the same timezone before comparison
                if start_date <= entry_date <= end_date and date_entry and in_process_date:
                    if status != 'Unprocessed':
                        total_complaints += 1
                    response_time = calculate_working_hours(date_entry, in_process_date)
                    total_response_time += response_time

            if total_complaints > 0:
                average_response_time = total_response_time / total_complaints
            else:
                average_response_time = 0

            final_result[range_name] = average_response_time

        # Add the final_result to office_data
        office_data['average_response_time'] = final_result
        query = f"""
            SELECT
                COUNT(*) AS number_of_complaints_resolved
            FROM
                complaints c
            WHERE
                c.status = 'Completed' AND c.reference_number IN (
                    SELECT employee_id FROM employees WHERE office_id = {office_data['office_id']}
                ) AND c.closed_date IS NOT NULL
                AND c.closed_date BETWEEN %s AND %s;
        """

        final_result = {}

        # Execute the query and process results for each date range
        for range_name, (start_date, end_date) in date_ranges.items():
            cursor.execute(query, (start_date, end_date))
            resolved_complaints_data = cursor.fetchone()

            if resolved_complaints_data:
                resolved_complaints_count = resolved_complaints_data[0]
            else:
                resolved_complaints_count = 0

            final_result[range_name] = resolved_complaints_count

        # Add the final_result to office_data
        office_data['total_complaints_resolved'] = final_result

        query = f"""
            SELECT
                COUNT(*) AS number_of_bounced_complaints
            FROM
                complaints c
            WHERE
                c.status IN ('Bounced', 'Bounced1', 'Bounced2') AND c.reference_number IN (
                    SELECT employee_id FROM employees WHERE office_id = {office_data['office_id']}
                ) AND c.bounced_date IS NOT NULL
                AND c.bounced_date BETWEEN %s AND %s;
        """

        final_result = {}

        # Execute the query and process results for each date range
        for range_name, (start_date, end_date) in date_ranges.items():
            cursor.execute(query, (start_date, end_date))
            bounced_complaints_data = cursor.fetchone()

            if bounced_complaints_data:
                bounced_complaints_count = bounced_complaints_data[0]
            else:
                bounced_complaints_count = 0

            final_result[range_name] = bounced_complaints_count

        # Add the final_result to office_data
        office_data['total_complaints_bounced'] = final_result
        employee_happiness_score = calculate_ehs(office_id)
        if employee_happiness_score:
            office_data["ehs_value"] = employee_happiness_score
        else:
            office_data["ehs_value"] = {}


        io_performance = calculate_io_performance(office_id)
        if io_performance:
            office_data["performance"] = io_performance
        else:
            office_data["performance"] = {}



        employee_safety_score = calculate_ess(office_id)
        if employee_safety_score:
            office_data["ess_value"] = employee_safety_score
        else:
            office_data["ess_value"] = {}


        complaints_query = f"""SELECT c.*
                    FROM complaints AS c
                    JOIN employees AS e ON c.reference_number = e.employee_id
                    WHERE e.office_id = {office_data['office_id']};"""





        if company_name in data:
            data[company_name].append(office_data)

        else:
            data[company_name] = [office_data]

    cursor.close()
    conn.close()
    return data


def add_new_buyer(buyer_name):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO buyers (buyer_name) VALUES (%s);", (buyer_name,))
        conn.commit()
        cursor.execute("SELECT buyer_id from buyers WHERE buyer_name = %s", (buyer_name,))
        buyer_id = cursor.fetchone()

        buyer_name_short = buyer_name.split(' ', 2)[0]
        enter_login(buyer_name_short, generate_random_password(8), 'admin', buyer_id[0])
        return True
    except Exception as e:
        print("Error:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def get_employee_data_for_fos_card(employee_id):
    conn = get_retryable_connection('complaints')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT employees.*, companies.name
        FROM employees
        JOIN offices ON employees.office_id = offices.office_id
        JOIN companies ON offices.company_id = companies.company_id
        WHERE employees.employee_id = %s
    """, (employee_id,))

    employee_data = cursor.fetchone()

    if employee_data:
        column_names = [desc[0] for desc in cursor.description]
        employee_dict = dict(zip(column_names, employee_data))
    else:
        employee_dict = None

    cursor.close()
    conn.close()

    return employee_dict




def update_buyer_name(buyer_id, buyer_name, username, password):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        passw = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(passw, bcrypt.gensalt())

        cursor.execute("SELECT id FROM logins WHERE access_id = %s AND role = 'admin'", (buyer_id,))
        id = cursor.fetchone()

        if id:
            id = id[0]
            cursor.execute("UPDATE buyers SET buyer_name = %s WHERE buyer_id = %s", (buyer_name, buyer_id))
            cursor.execute("UPDATE logins SET email = %s, password = %s WHERE access_id = %s AND role = 'admin'",
                           (username, hashed_password, buyer_id))
            conn.commit()
        return True
    except Exception as e:
        print("Error:", e)
        return False
    finally:
        cursor.close()
        conn.close()



def add_buyer_company(company_name, buyer_name):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        company_query = "SELECT company_id FROM companies WHERE name = %s"
        cursor.execute(company_query, (company_name,))
        company_id = cursor.fetchone()[0]

        buyer_query = "SELECT buyer_id FROM buyers WHERE buyer_name = %s"
        cursor.execute(buyer_query, (buyer_name,))
        buyer_id = cursor.fetchone()[0]

        insert_query = "INSERT INTO buyer_company (buyer_id, company_id) VALUES (%s, %s);"
        cursor.execute(insert_query, (buyer_id, company_id))

        conn.commit()
        return True

    except Exception as e:
        print("Error:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def update_employee_data(data):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        data['employee_id'] = int(data['employee_id'])
        update_query = (
            "UPDATE employees "
            "SET employee_name = %(employee_name)s, "
            "worker_type = %(worker_type)s, "
            "department = %(department)s, "
            "designation = %(designation)s, "
            "mobile_number = %(mobile_number)s, "
            "gender = %(gender)s, "
            "cnic_no = %(cnic_no)s "
            "WHERE employee_id = %(employee_id)s"
        )
        cursor.execute(update_query, data)
        conn.commit()
        return True

    except Exception as e:
        print("Error updating data:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def generate_ticket(complaint_category, curr_date, emp_id):
    conn = get_retryable_connection('complaints')
    cursor = conn.cursor()

    ticket_no = ""
    dict = {
        'Workplace Health, Safety and Environment': 'WS',
        'Freedom of Association': 'FA',
        'Child Labor': 'CL',
        'Wages & Benefits': 'WB',
        'Working Hours': 'WH',
        'Forced Labor': 'FL',
        'Discrimination': 'DR',
        'Unfair Employment': 'UE',
        'Ethical Business': 'EB',
        'Harassment': 'HR',
        'Workplace Discipline': 'DP',
        'Feedback': 'FB'
        
    }
    complaint_category = dict[complaint_category]

    select_query = """
        SELECT ticket_number
        FROM complaints
        ORDER BY date_entry DESC
        LIMIT 1
    """
    cursor.execute(select_query)
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        result = result[0]
        result = result[6:8]
        if result[0] == '0':
            result = int(result)+1
            result = "0" + str(result)
        elif result == '99':
            result = '00'
        else:
            result = int(result) + 1
        ticket_no = f"{complaint_category}{curr_date}{result}-{emp_id}"
    else:
        ticket_no = f"{complaint_category}{curr_date}00-{emp_id}"

    return ticket_no


def get_company_name_from_office_id(office_id):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        cursor.execute(f"""SELECT name from companies where company_id in 
        (SELECT company_id from offices where office_id = {office_id})""")
        company_name = cursor.fetchone()
        if company_name:
            return company_name[0]
        return None
    except:
        return None
    finally:
        cursor.close()
        conn.close()


def format_cnic(cnic):
    return cnic[:5] + '-' + cnic[5:12] + '-' + cnic[12:]

def retrieve_employee_data(employee_id):
    conn = get_retryable_connection('complaints')
    cursor = conn.cursor()
    employee_id = re.sub(r'\D', '', employee_id)
    try:
        if len(employee_id) == 13:
            formatted_cnic = format_cnic(employee_id)
            sql_query = """
            SELECT employee_id, employee_name, worker_type, department, designation, mobile_number, gender, office_id,employee_left
            FROM employees
            WHERE cnic_no = %s OR cnic_no = %s
            LIMIT 1
            """
            print('It is a cnic ',employee_id)
            cursor.execute(sql_query, (formatted_cnic,employee_id,))

        else:
            sql_query = """
                SELECT employee_id, employee_name, worker_type, department, designation, mobile_number, gender, office_id,employee_left
                FROM employees
                WHERE employee_id = %s
                LIMIT 1
            """
            cursor.execute(sql_query, (employee_id,))

        row = cursor.fetchone()

        if row:
            employee_id, employee_name, worker_type, department, designation, mobile_number, gender, office_id, employee_left = row
            company_name = get_company_name_from_office_id(office_id)
            return {
                "employee_id": employee_id,
                "employee_name": employee_name,
                "worker_type": worker_type,
                "department": department,
                "designation": designation,
                "mobile_number": mobile_number,
                "gender": gender,
                "office_id": office_id,
                "company_name": company_name,
                "employee_left": employee_left
            }
        else:
            cursor.close()
            conn.close()
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def retrieve_all_employee_data(search_value,length,start):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor(dictionary=True)

    # Base query
    query = """
    SELECT e.*, c.name AS company_name
    FROM employees e
    LEFT JOIN offices o ON e.office_id = o.office_id
    LEFT JOIN companies c ON o.company_id = c.company_id
    WHERE e.employee_left = 0
    """

    # Apply search if there's a value
    if search_value:
        query += f"""
        AND (e.employee_name LIKE '%{search_value}%'
        OR e.worker_type LIKE '%{search_value}%'
        OR e.department LIKE '%{search_value}%'
        OR e.designation LIKE '%{search_value}%'
        OR e.mobile_number LIKE '%{search_value}%'
        OR e.gender LIKE '%{search_value}%'
        OR c.name LIKE '%{search_value}%'
        OR e.cnic_no LIKE '%{search_value}%')
        """

    # Count total records
    cursor.execute(f"SELECT COUNT(*) as count FROM ({query}) as counted")
    total_records = cursor.fetchone()['count']

    # Count filtered records
    cursor.execute(f"SELECT COUNT(*) as count FROM ({query}) as counted")
    filtered_records = cursor.fetchone()['count']

    # Apply pagination
    query += f" LIMIT {length} OFFSET {start}"

    # Execute the final query
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    return total_records, filtered_records, result



def calculate_metrics_for_io_managers(buyer_id):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    io_managers_metrics = {}
    io_managers_query = f"""SELECT * FROM offices WHERE office_id IN  
            (SELECT office_id FROM companies WHERE company_id IN 
            (SELECT company_id FROM buyer_company WHERE buyer_id = {buyer_id}));"""

    # Fetch the IO Managers data into a pandas DataFrame
    io_managers_data = pd.read_sql_query(io_managers_query, conn)

    for i in range(len(io_managers_data)):
        io_manager_name = io_managers_data['office_name'].loc[i]

        complaints_query = f"""SELECT c.*
            FROM complaints AS c
            JOIN employees AS e ON c.reference_number = e.employee_id
            WHERE e.office_id = {io_managers_data['office_id'].loc[i]};"""

        complaints_data = pd.read_sql_query(complaints_query, conn)
        cursor.execute(f"""SElECT count(*) from employees where office_id = {io_managers_data['office_id'].loc[i]}""")
        total_employees = cursor.fetchone()
        total_employees = total_employees[0]
        io_manager_complaints_data = complaints_data[complaints_data["status"] != "Unprocessed"].copy()

        total_complaints_handled = io_manager_complaints_data.shape[0]
        total_complaints_bounced = io_manager_complaints_data['bounced_date'].notnull().sum()
        total_complaints_not_bounced = total_complaints_handled - total_complaints_bounced

        if total_complaints_handled > 0:
            average_satisfaction_rate = (total_complaints_not_bounced / total_complaints_handled) * 100
        else:
            average_satisfaction_rate = 0.0
        io_manager_complaints_data["in_process_date"] = pd.to_datetime(io_manager_complaints_data["in_process_date"])
        io_manager_complaints_data["date_entry"] = pd.to_datetime(io_manager_complaints_data["date_entry"])

        io_manager_complaints_data["response_time"] = (io_manager_complaints_data["in_process_date"] - io_manager_complaints_data["date_entry"]).dt.total_seconds() / 3600
        average_response_time = round(io_manager_complaints_data["response_time"].mean(),1)
        total_complaints_resolved = io_manager_complaints_data[io_manager_complaints_data["status"] == "Completed"].shape[0]

        io_managers_metrics[io_manager_name] = {
            "Total Employees":str(total_employees),
            "Total Complaints Handled": str(total_complaints_handled),
            "Average Satisfaction Rate": str(average_satisfaction_rate),
            "Average Response Time": str(average_response_time),
            "Total Complaints Resolved": str(total_complaints_resolved),
            "Total Complaints Bounced": str(total_complaints_bounced)
        }
    cursor.close()
    conn.close()
    return io_managers_metrics



def store_in_process_data(ticket_number, rca, capa, rca1, capa1, rca2, capa2, unprocess, username, user_ip, access_id, rca_datetime=None, rca1_datetime=None, rca2_datetime=None):
    curr_time = datetime.now(pakistani_tz)
    if rca_datetime:
            rca_datetime = datetime.strptime(rca_datetime, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
    if rca1_datetime:
        rca1_datetime = datetime.strptime(rca1_datetime, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
    if rca2_datetime:
        rca2_datetime = datetime.strptime(rca2_datetime, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
    query = """"""
    values = ()
    if unprocess:
        query = """
        UPDATE complaints SET status= 'In Process',in_process_date=%s WHERE ticket_number = %s"""
        values = (curr_time,ticket_number)
        insert_log_to_db(str(access_id),'IO Portal','Status Changed to In Process',user_ip,username,'',ticket_number)
    else:
        if rca and capa:
            # Update the complaint status to 'closed', set rca_time and capa_time
            query = """UPDATE complaints
                              SET status = 'Closed', closed_date = %s,rca=%s, rca_date = %s,rca_deadline = %s,capa=%s, capa_date = %s
                              WHERE ticket_number = %s"""
            values = (curr_time,rca, curr_time,rca_datetime,capa, curr_time, ticket_number)
            insert_log_to_db(str(access_id),'IO Portal','RCA and CAPA filled',user_ip,username,capa.split('.', 1)[0],ticket_number)
        if capa and not rca:
            # Update the complaint status to 'closed', set rca_time and capa_time
            query = """UPDATE complaints
                              SET status = 'Closed', closed_date = %s,capa=%s, capa_date = %s
                              WHERE ticket_number = %s"""
            values = (curr_time,capa, curr_time, ticket_number)
            insert_log_to_db(str(access_id),'IO Portal','CAPA filled',user_ip,username,capa.split('.', 1)[0],ticket_number)
        if rca and not capa:
            # Only update the rca_time
            query = """UPDATE complaints
                              SET rca=%s,rca_date = %s,rca_deadline=%s
                              WHERE ticket_number = %s"""
            values = (rca,curr_time,rca_datetime, ticket_number)
            insert_log_to_db(str(access_id),'IO Portal','RCA filled',user_ip,username,rca.split('.', 1)[0],ticket_number)
        if rca1 and capa1:
            # Update the complaint status to 'closed', set rca_time and capa_time
            query = """UPDATE complaints
                              SET status = 'Closed', closed_date = %s,rca1=%s, rca1_date = %s,capa1=%s, capa1_date = %s
                              WHERE ticket_number = %s"""
            values = (curr_time, rca1, curr_time, capa1, curr_time, ticket_number)  
            insert_log_to_db(str(access_id),'IO Portal','RCA1 and CAPA1 filled',user_ip,username,capa1.split('.', 1)[0],ticket_number)
        if rca1 and not capa1:
            # Only update the rca_time
            query = """UPDATE complaints
                              SET rca1=%s,rca_date = %s,rca1_deadline
                              WHERE ticket_number = %s"""
            values = (rca1, curr_time,rca1_datetime, ticket_number)
            insert_log_to_db(str(access_id),'IO Portal','RCA1 filled',user_ip,username,rca1.split('.', 1)[0],ticket_number)
        if capa1 and not rca1:
            # Update the complaint status to 'closed', set rca_time and capa_time
            query = """UPDATE complaints
                              SET status = 'Closed', closed_date = %s,capa1=%s, capa1_date = %s
                              WHERE ticket_number = %s"""
            values = (curr_time,capa1, curr_time, ticket_number)
            insert_log_to_db(str(access_id),'IO Portal','CAPA1 filled',user_ip,username,capa1.split('.', 1)[0],ticket_number)
        if rca2 and capa2:
            # Update the complaint status to 'closed', set rca_time and capa_time
            query = """UPDATE complaints
                              SET status = 'Closed', closed_date = %s,rca2=%s, rca2_date = %s,capa2=%s, capa2_date = %s
                              WHERE ticket_number = %s"""
            values = (curr_time, rca2, curr_time, capa2, curr_time, ticket_number)
            insert_log_to_db(str(access_id),'IO Portal','RCA2 and CAPA2 filled',user_ip,username,capa2.split('.', 1)[0],ticket_number)
        if capa1 and not rca1:
            # Update the complaint status to 'closed', set rca_time and capa_time
            query = """UPDATE complaints
                              SET status = 'Closed', closed_date = %s,capa2=%s, capa2_date = %s
                              WHERE ticket_number = %s"""
            values = (curr_time,capa2, curr_time, ticket_number)
            insert_log_to_db(str(access_id),'IO Portal','CAPA2 filled',user_ip,username,capa2.split('.', 1)[0],ticket_number)
        if rca2 and not capa2:
            # Only update the rca_time
            query = """UPDATE complaints
                              SET rca2=%s,rca_date = %s,rca2_deadline
                              WHERE ticket_number = %s"""
            values = (rca2, curr_time,rca2_datetime, ticket_number)
            insert_log_to_db(str(access_id),'IO Portal','RCA2 filled',user_ip,username,rca2.split('.', 1)[0],ticket_number)
    conn = get_retryable_connection('io')
    cursor = conn.cursor()
    try:
        cursor.execute(query, values)
        print("DOne")
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error:", e)
        conn.rollback()
        cursor.close()
        conn.close()




def export_mysql_to_excel(table_name):
    conn = get_retryable_connection('personal')
    # Establish a connection to the MySQL database

    # Read the data from MySQL into a pandas DataFrame
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)



    # Save the DataFrame to an Excel file
    df.to_excel(table_name + '.xlsx', index=False)
    print(f"Data from table '{table_name}' exported to '{table_name}'.")
    conn.close()
import bcrypt


def enter_login(username, passw, role, access_id):
    global cursor
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    password = passw.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    def get_unique_username(base_username):
        counter = 1
        new_username = base_username.lower()
        while True:
            try:
                cursor.execute("SELECT 1 FROM logins WHERE email = %s", (new_username,))
                if not cursor.fetchone():
                    return new_username
                new_username = f"{base_username.lower()}_{counter}"
                counter += 1
            except Exception as e:
                print(f"Error checking username: {e}")
                return None

    unique_username = get_unique_username(username)
    if not unique_username:
        print("Failed to generate a unique username")
        cursor.close()
        conn.close()
        return False

    insert_query = "INSERT INTO logins (email, password, role, access_id) VALUES (%s, %s, %s, %s)"
    values = (unique_username, hashed_password, role, access_id)

    try:
        cursor.execute(insert_query, values)
        conn.commit()
        
        email_thread = threading.Thread(target=send_login_password_email, args=(unique_username, passw))
        email_thread.start()
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error inserting login: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        return False




def verify_user(user,password):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    try:
        query = "SELECT password,role,access_id FROM logins WHERE email = %s"
        cursor.execute(query, (user,))
        row = cursor.fetchone()
        if row:
            stored_hashed_password = row[0].encode('utf-8')

            # Verify the password
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                return row[1],row[2]  # Password is correct
            else:
                return False  # Password is incorrect
        else:
            return False  # User not found

    except Exception as e:
        print("Error:", e)
        return False
    cursor.close()
    conn.close()
def insert_log_to_db(access_id,portal_name,action,ip_address,username,relevant_data,ticket_number):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    try:
        sql = """INSERT INTO app_logs (timestamp, user_id,portal_name,action,ip_address,username,relevant_data,ticket_number)
         VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (access_id,portal_name,action,ip_address,username,relevant_data,ticket_number))
        conn.commit()
    except Exception as e:
        print("Error inserting log:", e)
    cursor.close()
    conn.close()
def get_all_logs():
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    try:
        sql = "SELECT timestamp, level, message FROM app_logs"
        cursor.execute(sql)
        logs = []

        for row in cursor.fetchall():
            log = {
                "timestamp": row[0],
                "level": row[1],
                "message": row[2]
            }
            logs.append(log)

        return logs
    except Exception as e:
        print("Error retrieving logs:", e)
        return []
    cursor.close()
    conn.close()



def generate_and_save_qr_image(employee_id,company_name, original_image_path='static/images/fos_card.png', base_url="https://www.fruitofsustainability.com/login"):
    try:
        employee_id = str(employee_id)
        company_name = str(company_name)
        profile_image_path = f'static/images/company_logos/{company_name}.jpg'
        files_in_company_logos = [f for f in os.listdir('static/images/company_logos') if os.path.isfile(os.path.join('static/images/company_logos', f))]

        for files in files_in_company_logos:
            if company_name in files:
                profile_image_path = f'static/images/company_logos/{files}'
        profile_image_path = 'static/images/company_logos/Denim-E.jpeg'
        # Generate the QR code data with the full URL
        data = f'{base_url}/employee/{employee_id}'
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=0,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="rgba(246, 243, 243, 0)").convert("RGBA")

        # Open the original image and convert to RGBA mode
        base_image = Image.open(original_image_path).convert("RGBA")
        
        # Overlay the QR code onto the base image
        box_width = 145
        box_height = 145
        box_position = (base_image.width - box_width - 25, base_image.height - box_height - 20)
        qr_image_resized = qr_image.resize((box_width-10, box_height-10))
        base_image.paste(qr_image_resized, box_position, qr_image_resized)
        
        # Add the employee ID as text to the image
        font = ImageFont.truetype('static/BodoniFLF.ttf', 60)
        print('yes')
        draw = ImageDraw.Draw(base_image)
        text_color = (58, 48, 42)  # Black color
        text_position = (300, 200)
        
        draw.text(text_position, str(employee_id), font=font, fill=text_color)
        
        # Overlay the profile image (e.g., company logo) on top right
        profile_image = Image.open(profile_image_path).convert("RGBA")
        profile_size = (box_width, box_height)
        profile_image_resized = profile_image.resize(profile_size)
        profile_position = (base_image.width - profile_size[0] - 40, 35)
        base_image.paste(profile_image_resized, profile_position, profile_image_resized)

        # Save the modified image
        output_directory = "static/images/card_images"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        output_file_path = os.path.join(output_directory, f"employee_{employee_id}.png")
        base_image.save(output_file_path)
        
        return output_file_path
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

def get_last_fos_id():
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    cursor.execute("""SELECT employee_id
    FROM employees
    ORDER BY employee_id DESC
    LIMIT 1;""")
    last_id = cursor.fetchone()
    last_id = last_id[0]
    conn.close()
    return last_id

def generate_employee_ids(row, last_employee_id):
    
    company_id = int(row['office_id'])
    if company_id > 71 and company_id < 85:
        company_id  = 86
    elif company_id > 84 and company_id < 98:
        company_id  = 87
    elif company_id > 97 and company_id < 111:
        company_id  = 88
    elif (company_id > 145 and company_id < 181) or (company_id in range(225,230)):
        company_id  = 15
    elif company_id in range(123,141):
        company_id =44
    gender = row['gender']
    worker_type = row['worker_type']

    employee_id = str(company_id)

    if gender.lower() == 'male' and worker_type.lower() == 'staff':
        employee_id += str(random.randrange(1, 5, 2))
    elif gender.lower() == 'male' and worker_type.lower() in ['labor','labour']:
        employee_id += str(random.randrange(2, 5, 2))
    elif gender.lower() == 'female' and worker_type.lower() == 'staff':
        employee_id += str(random.randrange(5, 9, 2))
    elif gender.lower() == 'female' and worker_type.lower() in ['labor','labour']:
        employee_id += str(random.randrange(6, 9, 2))
    else:
        employee_id += str(random.randint(1, 9))
    last_employee_id = str(int(last_employee_id)+1)
    last_id = last_employee_id[-3:-1] + last_employee_id[-1]
    employee_id += last_id

    return int(employee_id)

def is_employee_present(cnic_no):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()

    try:
        select_query = "SELECT * FROM employees WHERE cnic_no = %s"
        cursor.execute(select_query, (cnic_no,))
        count = cursor.fetchone()
        if count:
            # If a record is found, employee is present
            return True
        else:
            # If no record is found, employee is not present
            return False
    except mysql.connector.Error as err:
        print("Error checking employee presence:", err)
        return False

    finally:
        cursor.close()
        conn.close()
        
def update_employee_in_database(employee_data):
    conn = get_retryable_connection('personal')
    cursor = conn.cursor()
    success = False

    try:
        # Replace NaN values with None for database insertion
        cleaned_employee_data = {k: None if pd.isna(v) else v for k, v in employee_data.items()}

        update_query = """
        UPDATE employees SET
        employee_name = %s,
        worker_type = %s,
        department = %s,
        designation = %s,
        mobile_number = %s,
        gender = %s,
        office_id = %s,
        company_id = %s
        WHERE cnic_no = %s
        """
        
        # Get the current time in the Pakistan timezone
        pakistan_tz = pytz.timezone('Asia/Karachi')
        entry_date = datetime.now(pakistan_tz).strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute(update_query, (
            cleaned_employee_data['employee_name'],
            cleaned_employee_data['worker_type'],
            cleaned_employee_data['department'],
            cleaned_employee_data['designation'],
            cleaned_employee_data['mobile_number'],
            cleaned_employee_data['gender'],
            cleaned_employee_data['office_id'],
            cleaned_employee_data['company_id'],
            cleaned_employee_data['cnic_no']  # Assuming this is the primary key
        ))
        
        conn.commit()
        success = True

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()
    except Exception as e:
        print(f"Unexpected error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return success
import json
from mysql.connector import Error

def get_all_surveys(access_id=None):
    connection = get_retryable_connection('personal')
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            if access_id:
                if access_id == 16:
                    query = """
                    SELECT DISTINCT s.id, s.title, s.description, s.question_count, s.estimated_time, s.created_at, s.expiry_date,
                    sf.filter_type, sf.filter_values
                    FROM surveys s
                    JOIN survey_filters sf ON s.id = sf.survey_id
                    JOIN employees e ON 1=1
                    JOIN offices o ON e.office_id = o.office_id
                    JOIN companies c ON o.company_id = c.company_id
                    LEFT JOIN buyer_company ON c.company_id = buyer_company.company_id
                    LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
                    WHERE s.buyer_id IN (15, 16)
                    """
                    cursor.execute(query)
                else:
                    query = """
                    SELECT DISTINCT s.id, s.title, s.description, s.question_count, s.estimated_time, s.created_at, s.expiry_date,
                    sf.filter_type, sf.filter_values
                    FROM surveys s
                    JOIN survey_filters sf ON s.id = sf.survey_id
                    JOIN employees e ON 1=1
                    JOIN offices o ON e.office_id = o.office_id
                    JOIN companies c ON o.company_id = c.company_id
                    LEFT JOIN buyer_company ON c.company_id = buyer_company.company_id
                    LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
                    WHERE s.buyer_id = %s
                    """
                    cursor.execute(query, (access_id,))
            else:
                query = """
                SELECT s.id, s.title, s.description, s.question_count, s.estimated_time, s.created_at, s.expiry_date,
                        sf.filter_type, sf.filter_values
                FROM surveys s
                LEFT JOIN survey_filters sf ON s.id = sf.survey_id
                """
                cursor.execute(query)
            
            rows = cursor.fetchall()
            
            surveys = {}
            for row in rows:
                survey_id = row['id']
                if survey_id not in surveys:
                    surveys[survey_id] = {
                        'id': survey_id,
                        'title': row['title'],
                        'description': row['description'],
                        'question_count': row['question_count'],
                        'estimated_time': row['estimated_time'],
                        'created_at': row['created_at'],
                        'date_expiry': row['expiry_date'],
                        'filters': []
                    }
                if row['filter_type'] is not None:
                    surveys[survey_id]['filters'].append({
                        'filter_type': row['filter_type'],
                        'filter_values': json.loads(row['filter_values'])
                    })
            
            return list(surveys.values())
        
        except Error as e:
            print(f"Error: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()
    else:
        return []

import os
import re
from mysql.connector import Error

def get_all_surveys_for_dashboard(access_id=None):
    connection = get_retryable_connection('personal')
    surveys = []
    if access_id == 16:
        buyer_ids = [15,16]
    else:
        buyer_ids = [access_id]
    print('Buyer ID for Survey: ',buyer_ids)


    # Fetch surveys from database
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            placeholders = ', '.join(['%s'] * len(buyer_ids))
            query = f"""
            SELECT DISTINCT s.id, s.title, s.created_at, s.buyer_id
            FROM surveys s
            JOIN employees e ON 1=1
            JOIN offices o ON e.office_id = o.office_id
            JOIN companies c ON o.company_id = c.company_id
            LEFT JOIN buyer_company ON c.company_id = buyer_company.company_id
            LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
            WHERE s.buyer_id IN ({placeholders})
            """
            cursor.execute(query, tuple(buyer_ids))
            rows = cursor.fetchall()
            for row in rows:
                row['created_at'] = row['created_at'].strftime('%Y-%m-%d')
                surveys.append({
                    'id': row['id'],
                    'title': row['title'],
                    'created_at': row['created_at'],
                    'buyer_id': row['buyer_id'],
                    'from_database': True
                })
        
        except Error as e:
            print(f"Error: {e}")
        
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()
    if 16 in buyer_ids:
        buyer_ids = [access_id]
    print('Buyer ID for Survey: ',buyer_ids)

    # Fetch surveys from survey_reports folder
    reports_directory = 'static/survey_reports'
    survey_files = os.listdir(reports_directory)
    file_pattern = re.compile(r'survey_(\d+)_(.+)_(\d{4}-\d{2}-\d{2})_buyer_(\d+)\.(pdf|xlsx)')
    for file in survey_files:
        match = file_pattern.match(file)
        if match:
            survey_id, title, date, buyer_id, file_type = match.groups()
            survey_id = int(survey_id)
            buyer_id = int(buyer_id)
            if buyer_id in buyer_ids:
                existing_survey = next((s for s in surveys if s['id'] == survey_id), None)
                if existing_survey:
                    existing_survey[file_type] = file
                else:
                    surveys.append({
                        'id': survey_id,
                        'title': title.replace('_', ' '),
                        'created_at': date,
                        'buyer_id': buyer_id,
                        file_type: file,
                        'from_database': False
                    })
    print('Surveys: ',surveys)

    return surveys

def delete_survey_from_db(survey_id):
    connection = get_retryable_connection('personal')
    if connection is not None:
        try:
            cursor = connection.cursor()

            # Delete filters first (due to foreign key constraint)
            delete_filters_query = "DELETE FROM survey_filters WHERE survey_id = %s"
            cursor.execute(delete_filters_query, (survey_id,))

            # Delete survey
            delete_survey_query = "DELETE FROM surveys WHERE id = %s"
            cursor.execute(delete_survey_query, (survey_id,))

            connection.commit()
            cursor.close()
            connection.close()

            return True, "Survey deleted successfully"

        except Exception as e:
            print(f"The error '{e}' occurred")
            return False, "Failed to delete survey"

    else:
        return False, "Database connection failed"
def fetch_all_departments(access_id = None):
    connection = get_retryable_connection('personal')
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            if access_id:
                query = """SELECT DISTINCT department FROM employees
                WHERE office_id IN 
                (SELECT office_id FROM offices WHERE company_id IN 
                 (SELECT company_id from companies where company_id IN
                (SELECT company_id FROM buyer_company WHERE buyer_id = %s)))"""
                cursor.execute(query, (access_id,))
            else:
                query = "SELECT DISTINCT department FROM employees"  # Adjust table and column names as needed
                cursor.execute(query)
            departments = [row['department'] for row in cursor.fetchall()]
            cursor.close()
            connection.close()
            return departments
        except Error as e:
            print(f"Error fetching departments: {e}")
            return []
    else:
        return []
def edit_survey_in_db(survey_id, data):
    connection = get_retryable_connection('personal')
    if connection is not None:
        try:
            cursor = connection.cursor()

            # Update the survey
            update_survey_query = """
            UPDATE surveys
            SET title = %s, description = %s, question_count = %s, estimated_time = %s, expiry_date = %s
            WHERE id = %s
            """
            cursor.execute(update_survey_query, (
                data['title'], data['description'], data['question_count'], data['estimated_time'],
                data['date_expiry'], survey_id
            ))

            # Delete old filters
            delete_old_filters_query = """
            DELETE FROM survey_filters WHERE survey_id = %s
            """
            cursor.execute(delete_old_filters_query, (survey_id,))

            # Add new filters
            add_filter_query = """
            INSERT INTO survey_filters (survey_id, filter_type, filter_values)
            VALUES (%s, %s, %s)
            """
            for filter_type, filter_values in data['filters'].items():
                cursor.execute(add_filter_query, (
                    survey_id,
                    filter_type,
                    json.dumps(filter_values)
                ))

            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"The error '{e}' occurred")
            return False
    else:
        return False
def add_new_survey(data,buyer_id):
    connection = get_retryable_connection('personal')
    if connection is not None:
        try:
            cursor = connection.cursor()

            # Insert survey details
            add_survey_query = """
            INSERT INTO surveys (title, description, question_count, estimated_time, expiry_date,buyer_id)
            VALUES (%s, %s, %s, %s, %s,%s)
            """
            cursor.execute(add_survey_query, (
                data['title'],
                data['description'],
                data['question_count'],
                data['estimated_time'],
                data['expiry_date'],
                buyer_id
            ))
            survey_id = cursor.lastrowid

            # Insert filters
            add_filter_query = """
            INSERT INTO survey_filters (survey_id, filter_type, filter_values)
            VALUES (%s, %s, %s)
            """
            for filter_type, filter_values in data['filters'].items():
                if filter_values:
                    cursor.execute(add_filter_query, (
                        survey_id,
                        filter_type,
                        json.dumps(filter_values)
                    ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return {
                'id': survey_id,
                **data
            }
        
        except Exception as e:
            print(f"The error '{e}' occurred")
            return None
    
    else:
        return None

def delete_survey_from_db(survey_id):
    connection = get_retryable_connection('personal')
    if connection is not None:
        try:
            cursor = connection.cursor()

            # Delete filters first (due to foreign key constraint)
            delete_filters_query = "DELETE FROM survey_filters WHERE survey_id = %s"
            cursor.execute(delete_filters_query, (survey_id,))

            # Delete survey
            delete_survey_query = "DELETE FROM surveys WHERE id = %s"
            cursor.execute(delete_survey_query, (survey_id,))

            connection.commit()
            cursor.close()
            connection.close()

            return True, "Survey deleted successfully"

        except Exception as e:
            print(f"The error '{e}' occurred")
            return False, "Failed to delete survey"

    else:
        return False, "Database connection failed"
def fetch_all_departments(access_id = None):
    connection = get_retryable_connection('personal')
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            if access_id:
                query = """SELECT DISTINCT department FROM employees
                WHERE office_id IN 
                (SELECT office_id FROM offices WHERE company_id IN 
                 (SELECT company_id from companies where company_id IN
                (SELECT company_id FROM buyer_company WHERE buyer_id = %s)))"""
                cursor.execute(query, (access_id,))
            else:
                query = "SELECT DISTINCT department FROM employees"  # Adjust table and column names as needed
                cursor.execute(query)
            departments = [row['department'] for row in cursor.fetchall()]
            cursor.close()
            connection.close()
            return departments
        except Error as e:
            print(f"Error fetching departments: {e}")
            return []
    else:
        return []
def edit_survey_in_db(survey_id, data):
    connection = get_retryable_connection('personal')
    if connection is not None:
        try:
            cursor = connection.cursor()

            # Update the survey
            update_survey_query = """
            UPDATE surveys
            SET title = %s, description = %s, question_count = %s, estimated_time = %s, expiry_date = %s
            WHERE id = %s
            """
            cursor.execute(update_survey_query, (
                data['title'], data['description'], data['question_count'], data['estimated_time'],
                data['date_expiry'], survey_id
            ))

            # Delete old filters
            delete_old_filters_query = """
            DELETE FROM survey_filters WHERE survey_id = %s
            """
            cursor.execute(delete_old_filters_query, (survey_id,))

            # Add new filters
            add_filter_query = """
            INSERT INTO survey_filters (survey_id, filter_type, filter_values)
            VALUES (%s, %s, %s)
            """
            for filter_type, filter_values in data['filters'].items():
                cursor.execute(add_filter_query, (
                    survey_id,
                    filter_type,
                    json.dumps(filter_values)
                ))

            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"The error '{e}' occurred")
            return False
    else:
        return False





def fetch_all_offices(access_id = None):
    connection = get_retryable_connection('personal')  # Adjust database name as needed
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            if access_id:
                query = """SELECT offices.office_id, offices.office_name,companies.name FROM offices
                LEFT JOIN companies ON offices.company_id = companies.company_id
                WHERE companies.company_id IN 
                (SELECT company_id FROM buyer_company WHERE buyer_id = %s)"""
                cursor.execute(query, (access_id,))
            else:
                query = """SELECT offices.office_id, offices.office_name,companies.name FROM offices
                LEFT JOIN companies ON offices.company_id = companies.company_id"""
                cursor.execute(query)
            offices = cursor.fetchall()
            cursor.close()
            connection.close()
            return offices
        except Error as e:
            print(f"The error '{e}' occurred")
            return []
    else:
        return []


from mysql.connector import Error

def get_all_surveys_for_crud(access_id=None):
    connection = get_retryable_connection('personal')
    if connection is None:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        if access_id:
            if access_id == 16:
                query = """
                SELECT DISTINCT s.id, s.title, s.description, s.question_count, s.estimated_time, s.created_at, s.expiry_date
                FROM surveys s
                JOIN survey_filters sf ON s.id = sf.survey_id
                JOIN employees e ON 1=1
                JOIN offices o ON e.office_id = o.office_id
                JOIN companies c ON o.company_id = c.company_id
                LEFT JOIN buyer_company ON c.company_id = buyer_company.company_id
                LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
                WHERE s.buyer_id IN (15, 16)
                ORDER BY s.created_at DESC;
                """
                cursor.execute(query)
            else:
                query = """
                SELECT DISTINCT s.id, s.title, s.description, s.question_count, s.estimated_time, s.created_at, s.expiry_date
                FROM surveys s
                JOIN survey_filters sf ON s.id = sf.survey_id
                JOIN employees e ON 1=1
                JOIN offices o ON e.office_id = o.office_id
                JOIN companies c ON o.company_id = c.company_id
                LEFT JOIN buyer_company ON c.company_id = buyer_company.company_id
                LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
                WHERE s.buyer_id = %s
                ORDER BY s.created_at DESC;
                """
                cursor.execute(query, (access_id,))
        else:
            query = """
            SELECT id, title, description, question_count, created_at, expiry_date, estimated_time
            FROM surveys
            ORDER BY created_at DESC
            """
            cursor.execute(query)
        surveys = cursor.fetchall()
        return surveys
    except Error as e:
        print(f"Error while fetching surveys: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_question_to_db(question_data, instruction_media):
    connection = get_retryable_connection('personal')
    if connection is None:
        return False, "Database connection failed"
    print('Question Data:', json.dumps(question_data.get('options', [])))
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO survey_questions (survey_id, question_text, question_type, is_required, `order`, help_text, options)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            question_data['survey_id'],
            question_data['question_text'],
            question_data['question_type'],
            question_data['is_required'],
            question_data['order'],
            question_data['help_text'],
            question_data.get('options')  # Handle 'options' as JSON string
        )
        cursor.execute(query, values)
        connection.commit()
        
        instruction_media_path = None
        
        if instruction_media and instruction_media.filename != '':
            UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images/capa_images')

            filename = secure_filename(instruction_media.filename)
            filename_without_ext, file_extension = os.path.splitext(filename)
            # Custom filename based on survey ID and question ID
            filename = f'survey{question_data["survey_id"]}_question{cursor.lastrowid}{file_extension}'
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)  # Create directory if it does not exist
            instruction_media.save(filepath)
            instruction_media_path = filepath
            query = """
            UPDATE survey_questions SET image_url = %s WHERE question_id = %s
            """
            values = (
                filename,
                cursor.lastrowid
            )
            cursor.execute(query, values)
            connection.commit()
        
        cursor.close()
        connection.close()
        
        return True, "Question added successfully"
    
    except Exception as e:
        print(f"Error while adding question: {e}")
        return False, str(e)


def update_question_in_db(question_data):
    connection = get_retryable_connection('personal')
    if connection is None:
        return False, "Database connection failed"

    try:
        cursor = connection.cursor()
        query = """
        UPDATE survey_questions
        SET question_text = %s, question_type = %s, is_required = %s, `order` = %s, help_text = %s, options = %s
        WHERE question_id = %s
        """
        values = (
            question_data['question_text'],
            question_data['question_type'],
            question_data['is_required'],
            question_data['order'],
            question_data['help_text'],
            question_data.get('options'),  # Use .get() to handle cases where 'options' might not be present
            question_data['question_id']
        )
        cursor.execute(query, values)
        connection.commit()
        return True, "Question updated successfully"
    except Error as e:
        print(f"Error while updating question: {e}")
        return False, str(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


import json
from mysql.connector import Error

def get_all_survey_questions(access_id=None):
    connection = get_retryable_connection('personal')
    if connection is None:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        if access_id:
            if access_id == 16:
                query = """
                SELECT question_id, survey_id, question_text, question_type, 
                       is_required, `order`, help_text, options
                FROM survey_questions
                WHERE survey_id IN (
                    SELECT DISTINCT s.id
                    FROM surveys s
                    JOIN survey_filters sf ON s.id = sf.survey_id
                    JOIN employees e ON 1=1
                    JOIN offices o ON e.office_id = o.office_id
                    JOIN companies c ON o.company_id = c.company_id
                    LEFT JOIN buyer_company ON c.company_id = buyer_company.company_id
                    LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
                    WHERE s.buyer_id IN (15, 16))
                ORDER BY survey_id, `order`
                """
                cursor.execute(query)
            else:
                query = """
                SELECT question_id, survey_id, question_text, question_type, 
                       is_required, `order`, help_text, options
                FROM survey_questions
                WHERE survey_id IN (
                    SELECT DISTINCT s.id
                    FROM surveys s
                    JOIN survey_filters sf ON s.id = sf.survey_id
                    JOIN employees e ON 1=1
                    JOIN offices o ON e.office_id = o.office_id
                    JOIN companies c ON o.company_id = c.company_id
                    LEFT JOIN buyer_company ON c.company_id = buyer_company.company_id
                    LEFT JOIN buyers ON buyer_company.buyer_id = buyers.buyer_id
                    WHERE s.buyer_id = %s)
                ORDER BY survey_id, `order`
                """
                cursor.execute(query, (access_id,))
        else:
            query = """
            SELECT question_id, survey_id, question_text, question_type, 
                is_required, `order`, help_text, options
            FROM survey_questions
            ORDER BY survey_id, `order`
            """
            cursor.execute(query)
        
        questions = cursor.fetchall()
        
        # Parse JSON options
        for question in questions:
            if question['options']:
                question['options'] = json.loads(question['options'])
        
        return questions
    
    except Error as e:
        print(f"Error while fetching survey questions: {e}")
        return []
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_question_from_db(question_id):
    connection = get_retryable_connection('personal')
    if connection is None:
        return False, "Database connection failed"

    try:
        cursor = connection.cursor()
        query = "DELETE FROM survey_questions WHERE question_id = %s"
        cursor.execute(query, (question_id,))
        connection.commit()
        return True, "Question deleted successfully"
    except Error as e:
        print(f"Error while deleting question: {e}")
        return False, str(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def check_and_send_reminders():
    conn = None
    cursor = None
    try:
        # Database connection
        conn = get_retryable_connection('personal')
        cursor = conn.cursor(dictionary=True)
        current_time = datetime.now(pakistani_tz)
        # Query to get relevant complaints
        query = """
        SELECT complaint_no, ticket_number, status, in_process_date, rca, capa
        FROM complaints
        WHERE status IN ('In Process', 'Bounced', 'Bounced1')
        AND (rca IS NULL OR capa IS NULL OR capa1 IS NULL)
        AND in_process_date IS NOT NULL
        AND reference_number IN (SELECT employee_id FROM employees WHERE office_id BETWEEN 60 AND 71 OR office_id BETWEEN 221 AND 223)
        """
        
        # Check for complaints in the last 3 days
        cursor.execute(query)
        complaints = cursor.fetchall()
        print('complaints', complaints)
        for complaint in complaints:
            try:
                # Convert in_process_date to Pakistani time
                in_process_date = complaint['in_process_date'].replace(tzinfo=pytz.UTC).astimezone(pakistani_tz)
                time_elapsed = current_time - in_process_date
                print('Time elapsed:', time_elapsed)
                if timedelta(hours=48) < time_elapsed <= timedelta(hours=60):
                    # Send 48-hour reminder
                    recipient_email = 'imran.ijaz@cheezious.com'
                    elapsed_time = '48 hours'
                    person_name = 'Imran Ijaz'
                    send_reminder = True
                elif timedelta(hours=36) < time_elapsed <= timedelta(hours=48):
                    # Send 36-hour reminder
                    recipient_email = 'yousaf.basra@cheezious.com'
                    elapsed_time = '36 hours'
                    person_name = 'Yousuf Basra'
                    send_reminder = True
                else:
                    send_reminder = False
                if send_reminder:
                    # Send reminder email
                    email_sent = send_rca_capa_reminder_email(
                        recipient_email,
                        complaint['ticket_number'],
                        person_name,
                        elapsed_time
                    )
                    if not email_sent:
                        print(f"Failed to send reminder for ticket {complaint['ticket_number']}")
            except Exception as e:
                print(f"Error processing complaint {complaint['ticket_number']}: {e}")
    except Exception as e:
        print(f"Error in check_and_send_reminders: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def fetch_all_buyers():
    connection = get_retryable_connection('admin')
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT b.buyer_id, b.buyer_name
        FROM buyers b
        JOIN buyer_company bc ON b.buyer_id = bc.buyer_id
        GROUP BY b.buyer_id, b.buyer_name
        HAVING COUNT(DISTINCT bc.company_id) > 1 AND b.buyer_id NOT IN (16, 127, 182)
        """
        cursor.execute(query)
        buyers = cursor.fetchall()
        return buyers
    except Error as e:
        print(f"Error fetching buyers: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_companies_for_buyer(buyer_id):
    connection = get_retryable_connection('admin')
    if connection is None:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT c.company_id, c.name
        FROM companies c
        JOIN buyer_company bc ON c.company_id = bc.company_id
        JOIN buyers b ON bc.buyer_id = b.buyer_id
        WHERE bc.buyer_id = %s 
          AND (c.name = 'Cheezious' OR c.name != b.buyer_name)
        """
        cursor.execute(query, (buyer_id,))
        companies = cursor.fetchall()
        return companies
    except Error as e:
        print(f"Error fetching companies for buyer {buyer_id}: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_or_generate_summary(ticket_number, complaint_text):
    connection = get_retryable_connection('admin')
    if connection is None:
        return generate_summary(complaint_text)  # Fallback to generation if DB connection fails
    
    cursor = connection.cursor(dictionary=True)
    try:
        # Check if summary exists in database
        cursor.execute("SELECT feedback_summary FROM complaints WHERE ticket_number = %s", (ticket_number,))
        result = cursor.fetchone()
        
        if result and result['feedback_summary']:
            return result['feedback_summary']
        else:
            # Generate new summary
            summary = generate_summary(complaint_text)
            # Update database with new summary
            update_summary_in_db(connection, ticket_number, summary)
            return summary
    except Error as e:
        print(f"Database error: {e}")
        return generate_summary(complaint_text)  # Fallback to generation if DB query fails
    finally:
        cursor.close()
        connection.close()

def update_summary_in_db(connection, ticket_number, summary):
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE complaints SET feedback_summary = %s WHERE ticket_number = %s", (summary, ticket_number))
        connection.commit()
    except Error as e:
        print(f"Error updating summary in database: {e}")
        connection.rollback()
    finally:
        cursor.close()

def generate_summary(complaint_text):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(
            f"Generate a concise and informative title for the following complaint (MAX 6 words):\n{complaint_text}"
        )
        generated_text = response.text.strip()
        return generated_text
    except Exception as e:
        print(f"An error occurred while generating summary: {e}")
        return None
