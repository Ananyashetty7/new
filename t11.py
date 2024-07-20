import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",      # replace with your MySQL server host
            user="root",           # replace with your MySQL username
            password="Anigshetty@2004", # replace with your MySQL password
            database="t2"          # replace with your MySQL database name
        )
    except Error as e:
        st.error(f"The error '{e}' occurred")
    return connection

# Check user credentials
def check_credentials(username, password, role):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if role == "Admin":
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
    else:
        cursor.execute("SELECT * FROM Tourist WHERE EmailID=%s AND PhoneNo=%s", (username, password))
    user = cursor.fetchone()
    connection.close()
    return user

# Login function
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    role = st.sidebar.radio("Role", ["Admin", "Tourist"])

    if st.sidebar.button("Login"):
        user = check_credentials(username, password, role)
        if user:
            st.session_state["user"] = user
            st.session_state["role"] = role
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password")

# Admin dashboard
def admin_dashboard():
    st.title("Admin Dashboard")

    menu = ["Add Data", "View Data", "Update Data"]
    choice = st.selectbox("Menu", menu)

    if choice == "Add Data":
        st.subheader("Add Data")
        add_data()

    elif choice == "View Data":
        st.subheader("View Data")
        view_data()

    elif choice == "Update Data":
        st.subheader("Update Data")
        update_data()

# Add data function
def add_data():
    table = st.selectbox("Select Table", ["Tourist", "TourPackage", "Reservation", "Transportation", "Accommodation", "Payment"])
    if table == "Tourist":
        Name = st.text_input("Name")
        PhoneNo = st.text_input("PhoneNo")
        EmailID = st.text_input("EmailID")
        DOB = st.date_input("DOB")
        Age = st.number_input("Age", min_value=0)

        if st.button("Add Tourist"):
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Tourist (Name, PhoneNo, EmailID, DOB, Age) VALUES (%s, %s, %s, %s, %s)",
                           (Name, PhoneNo, EmailID, DOB, Age))
            connection.commit()
            connection.close()
            st.success("Tourist added successfully")

    # Similar code can be added for other tables (TourPackage, Reservation, etc.)

# View data function
def view_data():
    table = st.selectbox("Select Table", ["Tourist", "TourPackage", "Reservation", "Transportation", "Accommodation", "Payment"])
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    connection.close()

    st.write(data)

# Update data function
def update_data():
    table = st.selectbox("Select Table", ["Tourist", "TourPackage", "Reservation", "Transportation", "Accommodation", "Payment"])
    if table == "Tourist":
        TouristID = st.number_input("TouristID", min_value=0)
        Name = st.text_input("Name")
        PhoneNo = st.text_input("PhoneNo")
        EmailID = st.text_input("EmailID")
        DOB = st.date_input("DOB")
        Age = st.number_input("Age", min_value=0)

        if st.button("Update Tourist"):
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE Tourist SET Name=%s, PhoneNo=%s, EmailID=%s, DOB=%s, Age=%s WHERE TouristID=%s",
                           (Name, PhoneNo, EmailID, DOB, Age, TouristID))
            connection.commit()
            connection.close()
            st.success("Tourist updated successfully")

    # Similar code can be added for other tables (TourPackage, Reservation, etc.)

# Tourist dashboard
def tourist_dashboard():
    st.title("Tourist Dashboard")

    tourist_id = st.session_state["user"]["TouristID"]

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch tour packages
    cursor.execute("SELECT * FROM TourPackage")
    tour_packages = cursor.fetchall()

    st.subheader("Available Tour Packages")
    st.write(tour_packages)

    # Fetch reservations
    cursor.execute("SELECT * FROM Reservation WHERE TouristID=%s", (tourist_id,))
    reservations = cursor.fetchall()

    st.subheader("Your Reservations")
    st.write(reservations)

    # Fetch accommodations
    cursor.execute("""
        SELECT a.* FROM Accommodation a
        JOIN Reservation r ON a.BookingID = r.BookingID
        WHERE r.TouristID = %s
    """, (tourist_id,))
    accommodations = cursor.fetchall()

    st.subheader("Your Accommodations")
    st.write(accommodations)

    # Fetch transportations
    cursor.execute("""
        SELECT t.* FROM Transportation t
        JOIN Reservation r ON t.BookingID = r.BookingID
        WHERE r.TouristID = %s
    """, (tourist_id,))
    transportations = cursor.fetchall()

    st.subheader("Your Transportations")
    st.write(transportations)

    # Fetch payments
    cursor.execute("""
        SELECT p.* FROM Payment p
        JOIN Reservation r ON p.BookingID = r.BookingID
        WHERE r.TouristID = %s
    """, (tourist_id,))
    payments = cursor.fetchall()

    st.subheader("Your Payments")
    st.write(payments)

    connection.close()

# Main function
def main():
    st.title("Tour Management System")

    if "user" not in st.session_state:
        st.session_state["user"] = None

    if st.session_state["user"] is None:
        login()
    else:
        if st.session_state["role"] == "Admin":
            admin_dashboard()
        else:
            tourist_dashboard()

if __name__ == "__main__":
    main()
