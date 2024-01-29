import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyAOfMdEP3_CKEOZeNxs2kf4IyoOK8JTg78",
  'authDomain': "find-my-hostel-7b00e.firebaseapp.com",
  'projectId': "find-my-hostel-7b00e",
  'storageBucket': "find-my-hostel-7b00e.appspot.com",
  'messagingSenderId': "702444327414",
  'appId': "1:702444327414:web:027b634eaa869f2103f7d7",
  'measurementId': "G-8TPMQHL3L7",
  'databaseURL' : "https://find-my-hostel-7b00e-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()



def createUser(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return user
    except Exception as e:
        return 'Error Creating User'
def pushProvider(info):
    Name = info.pop(0)
    key = ['Hostel Name', 'First Name', 'Last Name','Email','Phone']
    data = dict(zip(key, info))
    
    db.child('Users').child('Provider').child(Name).child('Info').set(data)
    pass

def pushFinder(info):
    Name = info.pop(0)
    key = ['First Name', 'Last Name','Email','Phone']
    data = dict(zip(key, info))
    
    db.child('Users').child('Finder').child(Name).child('Info').set(data)

def login(email, password):
    try:
        status = auth.sign_in_with_email_and_password(email, password)
        return status
    except Exception as e:
        return "Error Loggin in!!"
def updateProvider(user,rooms, price):
    data={'Rooms':str(rooms),'Price':str(price)}
    db.child('Users').child('Provider').child(user).child('Details').set(data)
    pass
def database(user):
    data=db.child('Users').child('Provider').child(user).child('Details').get()
    return data.val()
def databasep():
    data = db.child('Users').child('Provider').get()
    return data.val()

