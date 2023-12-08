import mysql.connector
import streamlit as st
import datetime

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

st.header("Create Session", divider="blue")
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

# Session details input
selected_date = st.date_input("Select the date for your session")
selected_time = st.time_input("Select the time for your session")

# Combine date and time into a single datetime object
selected_datetime = datetime.datetime.combine(selected_date, selected_time)

# Current datetime for range check
now = datetime.datetime.now()

# Check if the selected datetime is in the past
if selected_datetime < now:
    st.error("Cannot select a date and time in the past. Please select a future date and time.")
else:
    if st.button("Confirm Session"):
        # Insert session details into the database
        insert_query = "INSERT INTO Sessions (PatientID, SessionTimestamp) VALUES (%s, %s)"
        mycursor.execute(insert_query, (patient_id, selected_datetime))
        mydb.commit()

        st.success("Your session has been scheduled successfully!")