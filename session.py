import streamlit as st
import datetime
import mysql.connector

def display_sessions(mycursor, patient_id,mydb):
    st.header("Your Booked Sessions")

    # Query to retrieve booked sessions
    mycursor.execute("SELECT SessionID, SessionTimestamp FROM Sessions WHERE PatientID = %s ORDER BY SessionTimestamp", (patient_id,))
    sessions = mycursor.fetchall()

    if not sessions:
        st.write("You have no sessions set up. Please create a new session.")
    else:
        for session in sessions:
            session_id, session_timestamp = session
            st.text(f"Session ID: {session_id}")
            st.text(f"Scheduled for: {session_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

            col1, col2 = st.columns(2)
            
            if col1.button("Modify", key=f"modify_{session_id}"):
                modify_session(mycursor,session_id,mydb)
            with col2:
                if st.button("Delete", key=f"delete_{session_id}"):
                    if st.button("Confirm Delete", key=f"confirm_delete_{session_id}"):
                        cancel_session(mycursor, session_id, mydb)


        st.markdown("---")

    if st.button("Create new Session"):
        create_session(mycursor, patient_id,mydb)

def create_session(mycursor,patient_id,mydb):
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

def modify_session(mycursor, session_id, mydb):
    # Get the existing session timestamp
    mycursor.execute("SELECT SessionTimestamp FROM Sessions WHERE SessionID = %s", (session_id,))
    current_timestamp = mycursor.fetchone()

    if current_timestamp:
        # Allow the user to modify the date and time
        st.write(f"Current session time: {current_timestamp[0]}")
        new_date = st.date_input("Select the new date for your session", current_timestamp[0].date())
        new_time = st.time_input("Select the new time for your session")

        # Combine the new date and time
        new_datetime = datetime.datetime.combine(new_date, new_time)
        now = datetime.datetime.now()

        if new_datetime < now:
            st.error("Cannot select a date and time in the past. Please select a future date and time.")
        else:
            if st.button("Confirm Changes"):
                # Update session details in the database
                update_query = "UPDATE Sessions SET SessionTimestamp = %s WHERE SessionID = %s"
                mycursor.execute(update_query, (new_datetime, session_id))
                mydb.commit()

                st.success("Your session has been updated successfully!")

def cancel_session(mycursor, session_id, mydb):
    # Confirmation before deletion
    if st.button("Confirm Delete", key=f"confirm_delete_{session_id}"):
        # Delete the session from the database
        delete_query = "DELETE FROM Sessions WHERE SessionID = %s"
        mycursor.execute(delete_query, (session_id,))
        mydb.commit()

        st.success("The session has been cancelled.")

