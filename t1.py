import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Database connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='tourism222',
            user='root',
            password='Anigshetty@2004'  # Replace with your actual MySQL root password
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            st.sidebar.success(f"Connected to MySQL Server version {db_info}")
            return connection
    except Error as e:
        st.sidebar.error(f"Error while connecting to MySQL: {e}")
        return None

# Fetch data function
def fetch_data(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Insert data function
def insert_data(connection, query, values):
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()

# Update data function
def update_data(connection, query, values):
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()

# Main Streamlit app
def main():
    st.title("Tourism Database")

    # Create database connection
    connection = create_connection()

    if connection:
        # Sidebar for admin interface
        st.sidebar.header("Admin Interface")
        option = st.sidebar.selectbox("Select an option", ["View Tourists", "Add Tourist", "Update Tourist"])

        if option == "View Tourists":
            st.header("Tourist Data")
            query = "SELECT * FROM Tourist"
            data = fetch_data(connection, query)
            if data:
                df = pd.DataFrame(data, columns=["TouristID", "Name", "DOB", "Age", "PhoneNo"])
                st.table(df)
            else:
                st.write("No data available.")

        elif option == "Add Tourist":
            st.header("Add New Tourist")
            tourist_id = st.number_input("Tourist ID", min_value=1, step=1)
            name = st.text_input("Name")
            dob = st.date_input("Date of Birth")
            age = st.number_input("Age", min_value=1, step=1)
            phone_no = st.text_input("Phone Number")

            if st.button("Add Tourist"):
                insert_query = """
                INSERT INTO Tourist (TouristID, Name, DOB, Age, PhoneNo)
                VALUES (%s, %s, %s, %s, %s)
                """
                insert_values = (tourist_id, name, dob, age, phone_no)
                insert_data(connection, insert_query, insert_values)
                st.success("Tourist added successfully!")

        elif option == "Update Tourist":
            st.header("Update Tourist Data")
            tourist_id = st.number_input("Enter Tourist ID to update", min_value=1, step=1)
            
            if st.button("Fetch Tourist Data"):
                fetch_query = "SELECT * FROM Tourist WHERE TouristID = %s"
                data = fetch_data(connection, fetch_query, (tourist_id,))
                if data:
                    name, dob, age, phone_no = data[0][1], data[0][2], data[0][3], data[0][4]
                    st.text_input("Name", value=name, key="update_name")
                    st.date_input("Date of Birth", value=dob, key="update_dob")
                    st.number_input("Age", value=age, step=1, key="update_age")
                    st.text_input("Phone Number", value=phone_no, key="update_phone_no")
                else:
                    st.error("No tourist found with that ID.")

            if st.button("Update Tourist"):
                update_name = st.session_state["update_name"]
                update_dob = st.session_state["update_dob"]
                update_age = st.session_state["update_age"]
                update_phone_no = st.session_state["update_phone_no"]
                
                update_query = """
                UPDATE Tourist 
                SET Name = %s, DOB = %s, Age = %s, PhoneNo = %s 
                WHERE TouristID = %s
                """
                update_values = (update_name, update_dob, update_age, update_phone_no, tourist_id)
                update_data(connection, update_query, update_values)
                st.success("Tourist updated successfully!")

        # Close the connection
        connection.close()

if __name__ == '__main__':
    main()