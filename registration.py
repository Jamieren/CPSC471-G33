import streamlit as st
import mysql.connector
from st_pages import Page, show_pages, add_page_title, hide_pages
import itertools
import streamlit as st
import hashlib

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Fishies_2002",
    database = "TPMS_471"
)

mycursor = mydb.cursor()
# Function to hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def match_therapist(primary_concerns, preferred_gender, preferred_specializations, preferred_mode):
    query = """
    SELECT * FROM Therapists
    WHERE Expertise = %s
    AND GenderPreference = %s
    AND Specialization = %s
    AND ModeOfTherapy = %s
    LIMIT 1
    """
    
    mycursor.execute(query, (primary_concerns, preferred_gender, preferred_specializations, preferred_mode))

    matched_therapist = mycursor.fetchone()
    return matched_therapist 
    

def form():
    st.title('Patient Account Creation')

    # Personal Information
    st.header('Personal Information')
    full_name = st.text_input('Full Name')
    email = st.text_input('Email Address')
    password = st.text_input('Password', type='password')
    age = st.number_input('Age', min_value=1, max_value=100)
    sex = st.selectbox('Sex', ['Male', 'Female', 'Other', 'Prefer not to say'])
    dob = st.date_input('Date of Birth')

    # Contact Information
    st.header('Contact Information')
    phone_number = st.text_input('Phone Number')
    address = st.text_input('Address (Optional)')

    # Mental Health Information
    st.header('Mental Health Information')
    primary_concerns = st.selectbox('Primary Concerns', ['Anxiety', 'Depression', 'Stress', 'Relationship Issues', 'Others'])
    therapy_goals = st.text_area('Therapy Goals')

    # Therapy Preferences
    st.header('Therapy Preferences')
    preferred_gender = st.selectbox('Preferred Gender of Therapist', ['Male', 'Female', 'No Preference'])
    preferred_specialization = st.selectbox('Preferred Specialization of Therapist', ['CBT', 'DBT', 'Psychoanalysis', 'Others'])
    preferred_mode = st.selectbox('Preferred Mode of Therapy', ['In-person', 'Online', 'Text-based'])

    # Additional Information
    st.header('Additional Information')
    language_preferences = st.text_input('Any specific language or cultural preferences? (Optional)')
    other_requirements = st.text_area('Any other preferences or requirements? (Optional)')

    consent = st.checkbox('I agree to the Terms of Service and Privacy Policy')

    if st.button('Create Account'):
        hashed_password = hash_password(password)  # Hashing the password
        
        # Insert into Users table
        sql_user = "INSERT INTO Users (Username, Password, UserType, Email) VALUES (%s, %s, %s, %s)"
        val_user = (full_name, hashed_password, 'Patient', email)
        mycursor.execute(sql_user, val_user)
        user_id = mycursor.lastrowid 

        # Insert into Patients table
        sql_patient = """
            INSERT INTO Patients (UserID, PsychologicalProfile, TherapyPreferences) 
            VALUES (%s, %s, %s)
        """
        psychological_profile = {
            'age': age,
            'sex': sex,
            'dob': dob.strftime('%Y-%m-%d'),  # Format date to string
            'primary_concerns': primary_concerns,
            'therapy_goals': therapy_goals
        }
        therapy_preferences = {
            'preferred_gender': preferred_gender,
            'preferred_specialization': preferred_specialization,
            'preferred_mode': preferred_mode,
            'language_preferences': language_preferences,
            'other_requirements': other_requirements
        }

        val_patient = (user_id, str(psychological_profile), str(therapy_preferences))
        mycursor.execute(sql_patient, val_patient)
        patient_id = mycursor.lastrowid  # Fetch the last inserted id for Patient

        mydb.commit()
        matched_therapist = match_therapist(
                    primary_concerns,
                    preferred_gender,
                    preferred_specialization,
                    preferred_mode,
                )
        
        if matched_therapist:
            print(matched_therapist)
            st.success("Matched with therapist!")
            therapist_id = matched_therapist[1]
            print("Debug - Therapist ID:", therapist_id)
            print("Debug - Patient ID:", patient_id)
            
            sql_match = "INSERT INTO Matches (TherapistID, PatientID) VALUES (%s, %s)"
            val_match = (therapist_id, patient_id)
            mycursor.execute(sql_match, val_match)
            
            mydb.commit()
            print(matched_therapist)
            st.write("Name:", matched_therapist[2])
            st.write("Expertise:", matched_therapist[3])
            st.write("Gender:", matched_therapist[4])
            st.write("Specialization:", matched_therapist[5])
            st.write("Mode of Therapy:", matched_therapist[6])
        else:
            st.error("No therapist matches your preferences at this time.")
        
        st.success("Patient account created successfully!", icon="😄")
        show_pages(
        [
            Page("create_session.py","Create Session", "🗓️"),
            Page("feedback.py", "Feedback","💌"),
            Page("chat.py", "Chat With Your Therapist","💬"),
            Page("dashboard.py", "Dashboard","💟"),
            Page("registration.py", "Registration", "⭐"),
        ]
        )
        # hide_pages(["Login"])

def main():
    st.session_state["username"] = st.session_state["username"]
    form()

if __name__ == "__main__":
    main()
