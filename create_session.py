import mysql.connector
import streamlit as st
import datetime


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Fishies_2002",
    database = "TPMS_471"
)

AVAILABLE_SLOTS = [
    '09:00:00', '10:00:00', '11:00:00', '12:00:00',
    '13:00:00', '14:00:00', '15:00:00', '16:00:00',
    '17:00:00'
]

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
         
def display_sessions(mycursor, mydb, patient_id):
    st.header("Your Booked Sessions")

    # Query to retrieve booked sessions
    mycursor.execute("SELECT SessionID, SessionDate, SessionTime FROM Sessions WHERE PatientID = %s AND IsBooked = True ORDER BY SessionDate, SessionTime", (patient_id,))
    sessions = mycursor.fetchall()

    if not sessions:
        st.write("You have no sessions set up. Please create a new session.")
    else:
        for session in sessions:
            session_id, session_date, session_time = session
            st.text(f"Session ID: {session_id}")
            st.text(f"Scheduled for: {session_date} at {session_time}")
            modify_key = f"modify_{session_id}"
            delete_key = f"delete_{session_id}"

            col1, col2 = st.columns(2)
            if col1.button("Modify", key=modify_key):
                st.session_state['modify_id'] = session_id
            if col2.button("Delete", key=delete_key):
                st.session_state['delete_id'] = session_id

        st.markdown("---")

    # Handle modification and deletion outside of the loop
    if 'modify_id' in st.session_state and st.session_state['modify_id']:
        modify_session(mycursor, st.session_state['modify_id'], mydb)
        #st.session_state['modify_id'] = None  # Reset the state

    if 'delete_id' in st.session_state and st.session_state['delete_id']:
        cancel_session(mycursor, st.session_state['delete_id'], mydb)
        st.session_state['delete_id'] = None  # Reset the state


def create_session(mycursor, patient_id, mydb):
    st.subheader("Book a New Session")

    # Step 1: Let the patient pick a date from the calendar
    selected_date = st.date_input("Select the date for your session", min_value=datetime.date.today())

    # Step 2: Query the database for the selected date's slots
    mycursor.execute("SELECT SessionTime, IsBooked FROM Sessions WHERE SessionDate = %s", (selected_date,))
    day_slots = mycursor.fetchall()

    # Convert day_slots to the correct format
    day_slots_dict = {}
    for slot, booked in day_slots:
        if isinstance(slot, datetime.time):  # Check if slot is a time object
            slot_str = slot.strftime("%H:%M:%S")
        else:
            # Handle timedelta or other types if necessary
            slot_str = str(slot)  # or convert timedelta to time, based on your logic
        day_slots_dict[slot_str] = booked


    # Step 3: Display all slots, marking those unavailable if already booked
    st.write("Please select a time slot:")
    for slot in AVAILABLE_SLOTS:
        start_time = datetime.datetime.strptime(slot, "%H:%M:%S").time()
        end_time = (datetime.datetime.strptime(slot, "%H:%M:%S") + datetime.timedelta(hours=1)).time()
        slot_str = f"{start_time.strftime('%I%p')} - {end_time.strftime('%I%p')}"

        if day_slots_dict.get(slot, 0):  # If the slot is booked
            st.write(f"{slot_str} - Not Available")
        else:
            if st.button(f"Book {slot_str}"):
                # Step 4: Book the slot if it's available
                if day_slots_dict.get(slot, 0):
                    st.error("Sorry, this slot is not available. Please choose a different one.")
                else:
                    insert_query = "INSERT INTO Sessions (PatientID, SessionDate, SessionTime, IsBooked) VALUES (%s, %s, %s, %s)"
                    mycursor.execute(insert_query, (patient_id, selected_date, start_time, 1))
                    mydb.commit()
                    st.success(f"Your session for {slot_str} has been booked successfully!")
                    break  # Exit the loop after booking to prevent multiple bookings
                
def modify_session(mycursor, session_id, mydb):
    st.subheader("Modify Your Session")

    # Allow the user to pick a new date
    new_date = st.date_input("Select the new date for your session", min_value=datetime.date.today())

    # Query the database for the selected date's slots, excluding the current session
    mycursor.execute(
        "SELECT SessionTime, IsBooked FROM Sessions WHERE SessionDate = %s AND SessionID <> %s",
        (new_date, session_id)
    )
    day_slots = mycursor.fetchall()

    # Convert day_slots to the correct format
    day_slots_dict = {}
    for slot, booked in day_slots:
        if isinstance(slot, datetime.time):  # Check if slot is a time object
            slot_str = slot.strftime("%H:%M:%S")
        else:
            slot_str = str(slot)  # Handle timedelta or other types
        day_slots_dict[slot_str] = booked

    # Display all slots, marking those unavailable if already booked
    st.write("Please select a new time slot:")
    for slot in AVAILABLE_SLOTS:
        slot_time = datetime.datetime.strptime(slot, "%H:%M:%S").time()
        slot_str = slot_time.strftime("%I%p-%I%p")
        if day_slots_dict.get(slot, 0):  # If the slot is booked
            st.write(f"{slot_str} - Not Available")
        else:
            if st.button(f"Change to {slot_str}"):
                # Update the session with the new date and time
                update_query = "UPDATE Sessions SET SessionDate = %s, SessionTime = %s WHERE SessionID = %s"
                mycursor.execute(update_query, (new_date, slot_time, session_id))
                mydb.commit()
                st.success(f"Your session has been changed to {new_date} at {slot_str}.")
                st.session_state['modify_id'] = None  # Reset the state
                st.rerun()
                #break  # Exit after the change to prevent multiple changes


        
def cancel_session(mycursor, session_id, mydb):

    delete_query = "DELETE FROM Sessions WHERE SessionID = %s"
    mycursor.execute(delete_query, (session_id,))
    mydb.commit()
    st.success("The session has been successfully deleted.")


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
        
display_sessions(mycursor,mydb, patient_id)
create_session(mycursor, patient_id, mydb)