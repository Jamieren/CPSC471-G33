import mysql.connector
import streamlit as st

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Fishies_2002",
    database = "TPMS"
)

mycursor = mydb.cursor()
print("Connection Established")

def main():
    st.title("Therapist Patient Matching System")

    option = st.sidebar.selectbox("Select an operation",("Create User", "Test2"))

    if option == "Create User":
        st.header("Create a User", divider="blue")
        username = st.text_input("Enter your username")
        password = st.text_input("Enter your password")
        email = st.text_input("Enter your email")
        user_type = st.radio("Select user type",("Therapist", "Patient"))

        if user_type == "Therapist":
            utype = "Therapist"
        if user_type == "Patient":
            utype = "Patient"

        if st.button("Create"):
            sql = "INSERT INTO Users(Username, Password, UserType, Email) values(%s, %s, %s, %s)"
            val = (username, password, utype, email)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("User created successfully!", icon = "😄")

    

if __name__ == "__main__":
    main()