import streamlit as st
import mysql.connector
import json

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ZxcZxc12",
    database="TPMS_471"
)
mycursor = mydb.cursor()

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

def get_user_details(user_id):
    query = "SELECT * FROM Users WHERE UserID = %s"
    mycursor.execute(query, (user_id,))
    return mycursor.fetchone()

def get_patient_details(patient_id):
    query = "SELECT * FROM Patients WHERE PatientID = %s"
    mycursor.execute(query, (patient_id,))
    return mycursor.fetchone()

def get_matched_therapist(patient_id):
    # Fetch matched therapist details
    query = """
    SELECT Therapists.* FROM Matches
    JOIN Therapists ON Matches.TherapistID = Therapists.TherapistID
    WHERE Matches.PatientID = %s
    """
    mycursor.execute(query, (patient_id,))
    result = mycursor.fetchone()

    # Logging for debugging
    print(f"Query executed for patient_id: {patient_id}")
    if result:
        print(f"Matched therapist details: {result}")
    else:
        print("No matched therapist found for this patient ID.")

    return result

def display_dashboard():
    st.title("Patient Dashboard")
    st.session_state["username"] = st.session_state["username"]
    p_user = st.session_state["username"]

    user_result = getUserID(p_user)
    user_id = user_result[0][0]  # Extract UserID from the first (and only) tuple
    patient_result = getpatientID(user_id)
    patient_id = patient_result[0][0]
    user_details = get_user_details(user_id)
    patient_details = get_patient_details(patient_id)
    therapist_details = get_matched_therapist(patient_id)
    st.subheader("Your Information")
    st.text(f"Name: {user_details[1]}")
    st.text(f"Email: {user_details[4]}")
    patient_info = json.loads(patient_details[2].replace("'", '"'))  # replacing single quotes with double quotes for valid JSON

    st.text(f"Age: {patient_info['age']}")
    st.text(f"Sex: {patient_info['sex']}")
    st.text(f"Primary Concerns: {patient_info['primary_concerns']}")
    st.text(f"Therapy Goals: {patient_info['therapy_goals']}")
    
    

    if therapist_details:
        st.subheader("Your Matched Therapist")
        st.text(f"Name: {therapist_details[2]}")
        st.text(f"Expertise: {therapist_details[3]}")
        st.text(f"Gender: {therapist_details[4]}")
        st.text(f"Specialization: {therapist_details[3]}")
        st.text(f"Mode of Therapy: {therapist_details[3]}")


    else:
        st.text("You do not have a matched therapist at the moment.")

if __name__ == "__main__":
    display_dashboard()