import streamlit as st
import mysql.connector
import hashlib
from st_pages import Page, show_pages, add_page_title, hide_pages

# Database connection setup
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="redacted",
    database="TPMS_471"
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
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    hide_decoration_bar_style = '''
            <style>
            header {visibility: hidden;}
            </style>
            '''
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
    st.title("🧩 MindMatch")
    st.header("Login")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type='password')
    if st.button('Login'):
        if verify_login(username, password):
            st.success('Login Successful!')
            show_pages(
                [
                    #Page("start.py", "Login", "🏠"),
                    Page("dashboard.py", "Dashboard","💟"),
                    Page("create_session.py","Sessions", "🗓️"),
                    Page("feedback.py", "Feedback","💌"),
                    Page("chat.py", "Chat With Your Therapist","💬"),
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
