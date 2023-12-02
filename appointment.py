import mysql.connector
import streamlit as st

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Fishies_2002",
    database = "TPMS_471"
)

mycursor = mydb.cursor()
print("Connection Established")

def search(username):
    sql = "SELECT * FROM Users WHERE Username = %s"
    val = (username,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    return result

def getSession(sessionID):
    sql = "SELECT * FROM Sessions WHERE SessionID = %s"
    val = (sessionID)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    return result

def getSessions(patientID):
    sql = "SELECT SessionID FROM Sessions WHERE PatientID = %s"
    val = (patientID)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    return result

def getPatients():
    mycursor.execute("SELECT PatientID FROM Patients")
    data = mycursor.fetchall()
    return data
    # return [value[0] for value in data]

def getTherapist(therapistID):
    sql = "SELECT * FROM Therapists WHERE TherapistID = %s"
    val = (therapistID,)
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

    option = st.sidebar.selectbox("Menu",("Create User", "View User", "Appointment", "Create Session"))

    if option == "Create User":
        st.header("Create a User (Development Only)", divider="blue")
        username = st.text_input("Enter your username")
        password = st.text_input("Enter your password", type="password")
        email = st.text_input("Enter your email")
        user_type = st.radio("Select user type",("Therapist", "Patient"))

        if user_type == "Therapist":
            utype = "Therapist"
            name = st.text_input("Enter your name")
            id = st.text_input("Enter your Therapist ID number")
            exp = st.selectbox("Select your expertise",("Anxiety","Depression","Stress","Relationship Issues","Others")) 
            special = st.selectbox("Select your specialization",("CBT","DBT","Psychoanalysis","Others"))

            g_opt = st.radio("Select your gender preference",("Male","Female","No Preference"))
            if g_opt == "Male":
                gender = "Male"
            if g_opt == "Female":
                gender = "Female"
            if g_opt == "No Preference":
                gender = "No Preference" 

            m_opt = st.radio("Select your mode of therapy",("In-person", "Online", "Text-based"))
            if m_opt == "In-person":
                mode = "In-person"
            if m_opt == "Online":
                mode = "Online"
            if m_opt == "Text-based":
                mode = "Text-based"

            if st.button("Create"):
                sql = "INSERT INTO Users(Username, Password, UserType, Email) VALUES(%s, %s, %s, %s)"
                val = (username, password, utype, email)
                mycursor.execute(sql, val)
                mydb.commit()

                user_id = mycursor.lastrowid

                sql_t = "INSERT INTO Therapists(UserID, TherapistID, Name, Expertise, GenderPreference, Specialization, ModeOfTherapy) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                val_t = (user_id, id, name, exp, gender, special, mode)
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

    if option == "Create Session":
        st.header("Create Session (Development Only)", divider="blue")
        t_id = st.text_input("Enter session's TherapistID")
        p_id = st.text_input("Enter session's PatientID")
        notes = st.text_area("Enter session's notes")

        if st.button("Create"):
            sql = "INSERT INTO Sessions(TherapistID, PatientID, Notes) VALUES(%s, %s, %s)"
            val = (t_id, p_id, notes)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Session created successfully!", icon = "😄")

    if option == "Appointment":
        # later make it so it says the appointment date in the header 
        st.header("Next Appointment Details", divider="blue")

        data = getPatients()
        ps_id = st.selectbox("Select a patientID", data)

        sessions = getSessions(ps_id)
        s_id = st.selectbox("Select a sessionID", sessions)
        # s_id = session [0][0]
        #st.write(s_id)

        session = getSession(s_id)
        #st.write(session)
        #print(type(s_id))
        session_id = s_id[0]
        #st.write(session_id)

        t_id = session[0][1]
        therapist = getTherapist(t_id)
        t_name = therapist[0][2]
        t_exp = therapist[0][3]
        t_sp = therapist[0][5]


        st.markdown(f":blue[**Therapist Name:**] {t_name}")
        st.markdown(f":blue[**Expertise:**] {t_exp}")
        st.markdown(f":blue[**Specialization:**] {t_sp}")

        # feedback form here as well
        st.subheader("Appointment Feedback")
        rating = st.slider("Rate your experience from 1 to 5",1, 5, 1)
        if rating == 1:
            st.markdown("<h3 style='text-align: center;'>⭐️</h3>", unsafe_allow_html=True)
        if rating == 2:
            st.markdown("<h3 style='text-align: center;'>⭐️⭐️</h3>", unsafe_allow_html=True)
        if rating == 3:
            st.markdown("<h3 style='text-align: center;'>⭐️⭐️⭐️</h3>", unsafe_allow_html=True)
        if rating == 4:
            st.markdown("<h3 style='text-align: center;'>⭐️⭐️⭐️⭐️</h3>", unsafe_allow_html=True)
        if rating == 5:
            st.markdown("<h3 style='text-align: center;'>⭐️⭐️⭐️⭐️⭐️</h3>", unsafe_allow_html=True)
        
        comment = st.text_area("Additional comments")

        if st.button("Submit"):
            # Check if feedback already exists for the session
            feedback_exists = False
            try:
                sql = "SELECT * FROM Feedback WHERE SessionID = %s"
                val = (session_id,)
                mycursor.execute(sql, val)
                existing_feedback = mycursor.fetchall()
                if existing_feedback:
                    feedback_exists = True
            except Exception as e:
                st.error(f"Error checking existing feedback: {str(e)}")

            if feedback_exists:
                st.warning("Feedback has already been submitted for this session",icon="😉")
            else:
                try:
                    # Insert new feedback into the database
                    sql = "INSERT INTO Feedback(SessionID, Rating, Comment) VALUES(%s, %s, %s)"
                    val = (session_id, rating, comment)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    st.success("Feedback submitted successfully! Thank you for your input", icon="😄")
                except Exception as e:
                    st.error(f"Error submitting feedback: {str(e)}")

if __name__ == "__main__":
    main()