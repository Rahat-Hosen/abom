import pyodbc
import json
import requests
from py4web import action, request, response
from py4web.utils.form import Form
from pydal.validators import *
from ..common import db, session, T, auth, flash
from datetime import datetime

# Define the action to retrieve data from SQL Server and send it to another endpoint
@action('test_conn/fetch_customer_data', method=['GET', 'POST'])
def fetch_customer_data():
    try:
        # Establish SQL Server connection
        conn = pyodbc.connect(
            "Driver={SQL Server};"
            "Server=localhost;"
            "Database=surjoDatabase;"
            "UID=sa;"
            "PWD=;"
            "Trusted_Connection=yes;"
        )
        print("Connection successful")

        # Fetch data from SQL Server
        cursor = conn.cursor()
        select_query = """
        SELECT
        [name], [address], [second_address], [email], [city], [contact_person], [phone_number],
        [payment], [po_number], [vat], [dis_count], [credit_limit], [current_due], [accpac_code],
        [status] FROM [surjoDatabase].[dbo].[customers]
        """
        cursor.execute(select_query)

        # Fetch all rows
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            return "No data found"

        # Build bulk insert query for MySQL
        insert_query = "INSERT INTO client (name, address, second_address, email, city, contact_person, phone_number, payment, po_number, vat, dis_count, credit_limit, current_due, accpac_code, status) VALUES "

        # List to hold values for the bulk insert
        values_list = []
        for row in rows:
            values_list.append(
                "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                    row.name, row.address, row.second_address, row.email, row.city, row.contact_person, 
                    row.phone_number, row.payment, row.po_number, row.vat, row.dis_count, 
                    row.credit_limit, row.current_due, row.accpac_code, row.status
                )
            )

        # Final bulk insert query
        insert_query += ", ".join(values_list) + ";"
        
        # Execute bulk insert into MySQL
        db.executesql(insert_query)
        db.commit()  # Commit to the MySQL database

        return json.dumps({"status": "success", "message": "Data successfully inserted into MySQL!"})
    
    except pyodbc.Error as ex:
        print(f"SQL Server error: {ex}")
        return f"SQL Server Error: {ex}"

    except Exception as e:
        db.rollback()  # Rollback in case of error
        print(f"Unexpected error: {str(e)}")
        return json.dumps({"status": "error", "message": str(e)})


# Define action to fetch data from MySQL and insert into SQL Server
@action('test_conn/insert_into_sqlserver', method=['GET', 'POST'])
def insert_into_sqlserver():
    try:
        # Step 1: Fetch data from MySQL (client table in MySQL)
        select_query = """
        SELECT name, address, second_address, email, city, contact_person, phone_number, payment, po_number, vat, dis_count, credit_limit, current_due, accpac_code, status 
        FROM client
        """
        print("Fetching data from MySQL...")
        my_sql_data = db.executesql(select_query, as_dict=True)
        
        if not my_sql_data:
            return "No data found in MySQL"

        # Step 2: Establish SQL Server connection
        conn = pyodbc.connect(
            "Driver={SQL Server};"
            "Server=localhost;"
            "Database=surjoDatabase;"
            "UID=;"
            "PWD=;"  # Replace with your actual password
            "Trusted_Connection=yes;"
        )
        print("Connection to SQL Server successful")

        cursor = conn.cursor()

        # Step 3: Use parameterized queries to insert the data
        insert_query = """
        INSERT INTO [surjoDatabase].[dbo].[customers] 
        (name, address, second_address, email, city, contact_person, phone_number, payment, po_number, vat, dis_count, credit_limit, current_due, accpac_code, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Step 4: Execute the parameterized query for each row
        for row in my_sql_data:
            cursor.execute(insert_query, (
                row['name'], row['address'], row['second_address'], row['email'], row['city'], row['contact_person'],
                row['phone_number'], row['payment'], row['po_number'], row['vat'], row['dis_count'],
                row['credit_limit'], row['current_due'], row['accpac_code'], row['status']
            ))
        conn.commit()  # Commit the transaction

        cursor.close()
        conn.close()

        return json.dumps({"status": "success", "message": "Data successfully inserted into SQL Server!"})
    
    except pyodbc.Error as ex:
        print(f"SQL Server error: {ex}")
        return f"SQL Server Error: {ex}"

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return json.dumps({"status": "error", "message": str(e)})

    finally:
        if 'conn' in locals():
            conn.close()  # Close the SQL Server connection



