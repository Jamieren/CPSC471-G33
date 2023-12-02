import hashlib
import mysql.connector
import itertools
names = [
    "Liam", "Noah", "Oliver", "Elijah", "William", "James", "Benjamin", "Lucas", "Henry", "Alexander",
    "Mason", "Michael", "Ethan", "Daniel", "Jacob", "Logan", "Jackson", "Levi", "Sebastian", "Mateo",
    "Jack", "Owen", "Theodore", "Aiden", "Samuel", "Joseph", "John", "David", "Wyatt", "Matthew",
    "Luke", "Asher", "Carter", "Julian", "Grayson", "Leo", "Jayden", "Gabriel", "Isaac", "Lincoln",
    "Anthony", "Hudson", "Dylan", "Ezra", "Thomas", "Charles", "Christopher", "Jaxon", "Maverick", "Josiah",
    "Isaiah", "Andrew", "Elias", "Joshua", "Nathan", "Caleb", "Ryan", "Adrian", "Miles", "Eli",
    "Nolan", "Christian", "Aaron", "Cameron", "Ezekiel", "Colton", "Luca", "Landon", "Hunter", "Jonathan",
    "Santiago", "Axel", "Easton", "Cooper", "Jeremiah", "Angel", "Roman", "Connor", "Jameson", "Robert",
    "Greyson", "Jordan", "Ian", "Carson", "Jaxson", "Leonardo", "Nicholas", "Dominic", "Austin", "Everett",
    "Brooks", "Xavier", "Kai", "Jose", "Parker", "Adam", "Jace", "Wesley", "Kayden", "Silas",
    "Bennett", "Declan", "Waylon", "Weston", "Evan", "Emmett", "Micah", "Ryder", "Beau", "Damian",
    "Brayden", "Gael", "Rowan", "Harrison", "Bryson", "Sawyer", "Amir", "Kingston", "Jason", "Giovanni",
    "Vincent", "Ayden", "Chase", "Myles", "Diego", "Nathaniel", "Legend", "Jonah", "River", "Tyler",
    "Cole", "Braxton", "George", "Milo", "Zachary", "Ashton", "Luis", "Jasper", "Kaiden", "Adriel",
    "Gavin", "Bentley", "Calvin", "Zion", "Juan", "Maxwell", "Max", "Ryker", "Carlos", "Emmanuel",
    "Jayce", "Lorenzo", "Ivan", "Jude", "August", "Kevin", "Malachi", "Elliott", "Rhett", "Archer",
    "Karter", "Arthur", "Luka", "Elliot", "Thiago", "Brandon", "Camden", "Justin", "Jesus", "Maddox",
    "King", "Theo", "Enzo", "Matteo", "Emiliano", "Dean", "Hayden", "Finn", "Brody", "Antonio",
    "Abel", "Alex", "Tristan", "Graham", "Zayden", "Judah", "Xander", "Miguel", "Atlas", "Messiah"
]

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "ZxcZxc12",
    database = "TPMS_471"
)


mycursor = mydb.cursor()
# Function to hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_therapists():
    primary_concerns = ['Anxiety', 'Depression', 'Stress', 'Relationship Issues', 'Others']
    genders = ['Male', 'Female', 'No Preference']
    specializations = ['CBT', 'DBT', 'Psychoanalysis', 'Others']
    modes = ['In-person', 'Online', 'Text-based']

    all_combinations = list(itertools.product(primary_concerns, genders, specializations, modes))

    if len(names) < len(all_combinations):
        print("Warning: There are not enough names to cover all combinations.")
        return  
    
    therapist_id = 1  
    therapists = []
    for name, combination in zip(names, all_combinations):
        therapists.append({
            "therapist_id": therapist_id,
            "name": name,
            "expertise": combination[0],
            "gender": combination[1],
            "specialization": combination[2],
            "mode": combination[3]
        })
        therapist_id += 1
    
    for therapist in therapists:
        therapist_id = therapist['therapist_id'] 
        default_password = "default_password"
        default_username = f"{therapist['name']}_{therapist['therapist_id']}"  # Modified username
        default_email = f"{default_username.replace(' ', '').lower()}@therapy.com"

        # Check if the username already exists
        mycursor.execute("SELECT Username FROM Users WHERE Username = %s", (default_username,))
        if mycursor.fetchone() is not None:
            print(f"Username {default_username} already exists. Skipping.")
            continue

        # Insert into Users table
        sql_user = """
            INSERT INTO Users (Username, Password, UserType, Email) 
            VALUES (%s, %s, %s, %s)
        """
        val_user = (default_username, default_password, 'Therapist', default_email)

        try:
            mycursor.execute(sql_user, val_user)
            user_id = mycursor.lastrowid  # Fetch the last inserted id

            # Then, insert into Therapists table
            sql_therapist = """
                INSERT INTO Therapists (UserID, TherapistID, Name, Expertise, GenderPreference, Specialization, ModeOfTherapy) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            val_therapist = (user_id, therapist_id, therapist['name'], therapist['expertise'], therapist['gender'], therapist['specialization'], therapist['mode'])
            mycursor.execute(sql_therapist, val_therapist)
            print("done 2")

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            break  # or handle the error as appropriate

    mydb.commit()
    
create_therapists()