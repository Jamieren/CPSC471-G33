import mysql.connector
import streamlit as st
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ZxcZxc12",
    database="TPMS_471"
)
mycursor = mydb.cursor()

def create_session():
    st.header("Schedule Your Therapy Session")

     # Current datetime for range check
    now = datetime.datetime.now()
    
    # Session details input
    selected_date = st.date_input("Please choose the date for your session")
    selected_time = st.time_input("Please choose a time for your session")
    
    # Combine date and time into a single datetime object
    selected_datetime = datetime.datetime.combine(selected_date, selected_time)


    # Check if the selected datetime is in the past
    if selected_datetime < now:
        st.error("Cannot select a date and time in the past. Please select a future date and time.")
        return

    # Confirm button
    if st.button("Confirm Session"):
        # Convert selected date and time into a string format
        session_notes = f"Session scheduled for {selected_date} at {selected_time}"

        # Insert session details into the database
        insert_query = "INSERT INTO Sessions (PatientID, Notes) VALUES (%s, %s)"
        #check if the patientID contain any SQL SELECT DELETE 
        mycursor.execute(insert_query, (patient_id, session_notes))
        mydb.commit()

        # Retrieve the session ID of the newly created session
        session_id = mycursor.lastrowid

        # Display confirmation details including Session ID, Date, and Time
        st.success(f"Your session has been scheduled successfully! Session ID: {session_id}")
        st.info(f"Session Date: {selected_date}, Time: {selected_time}")
        
create_session()

