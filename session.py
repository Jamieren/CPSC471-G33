import streamlit as st
import datetime

class SessionPage:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb

    def display_sessions(self, patient_id):
        st.header("Your Booked Sessions")

        # Query to retrieve booked sessions
        self.mycursor.execute("SELECT SessionID, SessionTimestamp FROM Sessions WHERE PatientID = %s ORDER BY SessionTimestamp", (patient_id,))
        sessions = self.mycursor.fetchall()

        if not sessions:
            st.write("Seems like you have no sessions set up before. Please press the 'Create new Session' button to start the journey with us.")
        else:
            for session in sessions:
                session_id, session_timestamp = session
                st.text(f"Session ID: {session_id}")
                st.text(f"Scheduled for: {session_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

                if st.button("Modify", key=f"modify_{session_id}"):
                    self.modify_session(patient_id, session_id)
                if st.button("Delete", key=f"delete_{session_id}"):
                    self.cancel_session(session_id)

            st.markdown("---")  # Adds a visual separator between sessions

        if st.button("Create new Session"):
            self.create_session(patient_id)

    def create_session(self, patient_id):
        # Current datetime for range check
        now = datetime.datetime.now()

        # Session details input
        selected_date = st.date_input("Select the date for your session", min_value=now.date())
        selected_time = st.time_input("Select the time for your session")

        # Combine date and time into a single datetime object
        selected_datetime = datetime.datetime.combine(selected_date, selected_time)

        # Check if the selected datetime is in the past
        if selected_datetime < now:
            st.error("Cannot select a date and time in the past. Please select a future date and time.")
        else:
            if st.button("Confirm Session"):
                # Insert session details into the database
                insert_query = "INSERT INTO Sessions (PatientID, SessionTimestamp) VALUES (%s, %s)"
                self.mycursor.execute(insert_query, (patient_id, selected_datetime))
                self.mydb.commit()

                session_id = self.mycursor.lastrowid
                st.success(f"Your session has been scheduled successfully! Session ID: {session_id}")

    # Assume modify_session and cancel_session are correctly defined here
