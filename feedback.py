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

def getUserID(username):
    sql = "SELECT UserID FROM Users WHERE Username = %s"
    val = (username,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    return result

def getpatientID(userID):
    sql = "SELECT PatientID FROM Patients WHERE UserID = %s"
    val = (userID,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    return result

def getPatients():
    mycursor.execute("SELECT PatientID FROM Patients")
    data = mycursor.fetchall()
    return data
    # return [value[0] for value in data]

def getSessions(patientID):
    sql = "SELECT SessionID FROM Sessions WHERE PatientID = %s"
    val = (patientID,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    return result

def getSession(sessionID):
    sql = "SELECT * FROM Sessions WHERE SessionID = %s"
    val = (sessionID)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    return result

def getTherapist(therapistID):
    sql = "SELECT * FROM Therapists WHERE TherapistID = %s"
    val = (therapistID,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    return result

# later make it so it says the appointment date in the header 
st.header("Next Appointment Details", divider="blue")

# get logged in user's username
st.session_state["username"] = st.session_state["username"]
p_user = st.session_state["username"]
#st.write(p_user)

# get logged in user's userID
user_result = getUserID(p_user)
user_id = user_result[0][0]  # Extract UserID from the first (and only) tuple
#st.write(user_id)

# get logged in user's patientID
patient_result = getpatientID(user_id)
patient_id = patient_result[0][0]
#st.write(patient_id)

# get patient's sessions
sessions = getSessions(patient_id)
s_id = st.selectbox("Select a sessionID", sessions)

# get session information
session = getSession(s_id)
session_id = s_id[0]

# get session therapist information
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