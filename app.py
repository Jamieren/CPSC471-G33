import mysql.connector
import streamlit as st


from create_session import create_session

patient_id = 1 

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "fake",
    database = "TPMS"
)

mycursor = mydb.cursor()
print("Connection Established")

def main():
    
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
                sql = "INSERT INTO Users(Username, Password, UserType, Email) values(%s, %s, %s, %s)"
                val = (username, password, utype, email)
                mycursor.execute(sql, val)
                mydb.commit()

                user_id = mycursor.lastrowid

                sql_t = "INSERT INTO Therapists(UserID, LicenseNumber, Specialization, Biography) values(%s, %s, %s, %s)"
                val_t = (user_id, license, special, bio)
                mycursor.execute(sql_t, val_t)
                mydb.commit()

                st.success("Therapist user created successfully!", icon = "😄")

        if user_type == "Patient":
            utype = "Patient"
            profile = st.text_area("Enter your psychological profile")
            pref = st.text_input("What are your therapy preferences")

            if st.button("Create"):
                sql = "INSERT INTO Users(Username, Password, UserType, Email) values(%s, %s, %s, %s)"
                val = (username, password, utype, email)
                mycursor.execute(sql, val)
                mydb.commit()

                user_id = mycursor.lastrowid

                sql_p = "INSERT INTO Patients(UserID, PsychologicalProfile, TherapyPreferences) values(%s, %s, %s)"
                val_p = (user_id, profile, pref)
                mycursor.execute(sql_p, val_p)
                mydb.commit()
                st.success("Patient user created successfully!", icon = "😄")
                
    if option == "Create a Session":
        create_session(patient_id, mycursor, mydb)
        
    #if option == "Change a Session":
     #   change_session()


if __name__ == "__main__":
    main()
    
    