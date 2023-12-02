import mysql.connector
import streamlit as st
import datetime

"""
Assumptions:
    1.Patient ID: It's assumed that the patient's ID (patient_id) is known at the time of scheduling. 
        For simplicity, we'll start with patient_id as 1, but in a real-world application, 
        this should be dynamically retrieved based on the logged-in user's information.
    2.Database Connection: The mycursor and mydb arguments represent the database cursor and connection objects, respectively. 
    3.The details of the scheduled session, such as the date and time, will be stored as a text entry in the Notes field of the Sessions table.
    4. Availability Check: The current implementation does not check the availability of the therapist. 
        It is assumed that all time slots are available for booking. 
        In real life, we would need a system to track and verify the availability of therapists to prevent double bookings.


Details:
    1. The function will prompt the user to input a date and time for their therapy session.
    2. The user can only choose a date and time that is in the future, relative to the current date and time.
    3. Once the user confirms their choice, the function will insert a new record into the Sessions table,
        with the patient_id, and the chosen date and time will be recorded in the Notes field.
    4. After the record is inserted, the function will retrieve and display the unique SessionID assigned by the database, 
        along with the chosen date and time, confirming the successful booking to the user.
        
        
Limitations:
    1. The function does not currently support selecting a therapist. It's assumed that the therapist has already been matched or assigned.
    2. There is no check against double bookings; the system assumes all times are available.
    
"""

def create_session(patient_id, mycursor, mydb):
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
