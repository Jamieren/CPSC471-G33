import mysql.connector
import streamlit as st

from create_session import create_session


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = " ",
    database = "TPMS"
)

mycursor = mydb.cursor()
print("Connection Established")

def search(username):
    sql = "SELECT * FROM Users WHERE Username = %s"
    val = (username,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    return result

def main():
    hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
    '''
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
    
    st.title("Therapist Patient Matching System")

    option = st.sidebar.selectbox("Menu",("Create User","Create a Session", "Test2"))


    if option == "Create User":
        st.header("Create a User", divider="blue")
        username = st.text_input("Enter your username")
        password = st.text_input("Enter your password", type="password")
        email = st.text_input("Enter your email")
        user_type = st.radio("Select user type",("Therapist", "Patient"))

        if user_type == "Therapist":
            utype = "Therapist"
            license = st.text_input("Enter your license number")
            special = st.text_input("Enter your specialization")
            bio = st.text_area("Write a short bio")  

            if st.button("Create"):
                sql = "INSERT INTO Users(Username, Password, UserType, Email) VALUES(%s, %s, %s, %s)"
                val = (username, password, utype, email)
                mycursor.execute(sql, val)
                mydb.commit()

                user_id = mycursor.lastrowid

                sql_t = "INSERT INTO Therapists(UserID, LicenseNumber, Specialization, Biography) VALUES(%s, %s, %s, %s)"
                val_t = (user_id, license, special, bio)
                mycursor.execute(sql_t, val_t)
                mydb.commit()

                st.success("Therapist user created successfully!", icon = "😄")

        if user_type == "Patient":
            utype = "Patient"
            profile = st.text_area("Enter your psychological profile")
            pref = st.text_input("What are your therapy preferences")

            if st.button("Create"):
                sql = "INSERT INTO Users(Username, Password, UserType, Email) VALUES(%s, %s, %s, %s)"
                val = (username, password, utype, email)
                mycursor.execute(sql, val)
                mydb.commit()

                user_id = mycursor.lastrowid

                sql_p = "INSERT INTO Patients(UserID, PsychologicalProfile, TherapyPreferences) VALUES(%s, %s, %s)"
                val_p = (user_id, profile, pref)
                mycursor.execute(sql_p, val_p)
                mydb.commit()
                st.success("Patient user created successfully!", icon = "😄")
                
    if option == "Create a Session":
        create_session(patient_id, mycursor, mydb)
        
    #if option == "Change a Session":
     #   change_session()


    if option == "View User":
        st.header("Search for a User", divider="blue")
        search_un = st.text_input("Enter the username to search")

        if st.button("Search"):
            result = search(search_un)

            if(result):
                st.success("User found!")
                #st.write(result)
                user_n = result[0][1]
                user_t = result[0][3]
                user_e = result[0][4]
                st.markdown(f":blue[**Username:**] {user_n}")
                st.markdown(f":blue[**Type:**] {user_t}")
                st.markdown(f":blue[**Email:**] {user_e}")

            else:
                st.warning("User not found!")

if __name__ == "__main__":
    main()

