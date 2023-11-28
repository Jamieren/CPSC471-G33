import mysql.connector
import streamlit as st
import datetime

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
        create_session()

if __name__ == "__main__":
    main()
    
def create_session():
    st.subheader("Create a New Session")
    
    # Assuming PatientID is known and set, otherwise you would get it from the current session or a login system
    # patient_id = get_patient_id_from_login_session()
    # For demonstration purposes, we'll use a static value
    patient_id = st.text_input("Enter your Patient ID")

    if patient_id:
        # Query to get specializations from the Physician table.
        mycursor.execute("SELECT Specialization FROM Physician GROUP BY Specialization")
        # Fetch specializations and extract the specialization values from the tuples
        specializations = [specialization for (specialization,) in mycursor.fetchall()]
        selected_specialization = st.selectbox("Select Specialization", specializations)

        if selected_specialization:
            # Query the database for physicians with the selected specialization.
            mycursor.execute(
                """
                SELECT PhysicianID, CONCAT(FirstName, ' ', LastName, ' - ', Specialization) AS PhysicianName
                FROM Physician
                WHERE Specialization = %s
                """, (selected_specialization,)
            )
            physicians = mycursor.fetchall()
            physician_choices = {name: pid for pid, name in physicians}
            selected_physician_name = st.selectbox("Select Physician", options=list(physician_choices.keys()))

            if selected_physician_name:
                physician_id = physician_choices[selected_physician_name]

                # Query the database for the selected physician's available times.
                # Assuming the Availability column is a boolean indicating if the physician is available for a new appointment.
                mycursor.execute(
                    """
                    SELECT Availability FROM Physician
                    WHERE PhysicianID = %s AND Availability = 1
                    """, (physician_id,)
                )
                availability = mycursor.fetchone()[0]
                
                if availability:
                    selected_time = st.time_input("Select Time for Appointment")

                    if st.button("Book Session"):
                        # Assume the session date is today, you might want to let the patient choose a date.
                        session_date = datetime.now().date()
                        session_datetime = datetime.combine(session_date, selected_time)

                        # Insert the new appointment into the Schedules table.
                        sql_insert_appointment = """
                            INSERT INTO Schedules (PhysicianID, Date, Time)
                            VALUES (%s, %s, %s)
                        """
                        val_appointment = (physician_id, session_date, selected_time)
                        mycursor.execute(sql_insert_appointment, val_appointment)
                        mydb.commit()

                        # Retrieve the generated ApptID
                        appt_id = mycursor.lastrowid

                        # Update the Physician table to set the availability to false
                        sql_update_availability = """
                            UPDATE Physician
                            SET Availability = 0
                            WHERE PhysicianID = %s
                        """
                        mycursor.execute(sql_update_availability, (physician_id,))
                        mydb.commit()

                        st.success(f"Appointment ID {appt_id} booked successfully for Patient ID {patient_id} with {selected_physician_name} at {session_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    st.error("The selected physician is not available for a new appointment.")

                    