import streamlit as st
import mysql.connector
import hashlib
from st_pages import Page, show_pages, add_page_title, hide_pages

# Database connection setup
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "Fishies_2002",
    database = "TPMS_471"
)
mycursor = mydb.cursor()

def verify_login(username, password):
    # Function to verify login credentials
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    sql = "SELECT * FROM Users WHERE Username = %s AND Password = %s"
    val = (username, hashed_password)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    return result is not None

# Streamlit UI for login
def main():
    st.title("Login Page")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type='password')
    if st.button('Login'):
        if verify_login(username, password):
            st.success('Login Successful!')
            show_pages(
                [
                    Page("start.py", "Login", "🏠"),
                    Page("create_session.py","Create Session", "🗓️"),
                    Page("feedback.py", "Feedback","💌"),
                    Page("chat.py", "Chat With Your Therapist","💬"),
                    Page("dashboard.py", "Dashboard","💟"),
                ]
                )
        else:
            
            st.error('Username or Password is incorrect')

    # Add button and logic for new account creation
    new = st.button("Create New Account")
    if new:
        show_pages(
        [
            Page("registration.py", "Registration", "⭐"),
            Page("start.py", "Login", "🏠"),

        ]
        )

if __name__ == "__main__":
    main()