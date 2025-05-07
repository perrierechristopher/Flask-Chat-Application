import uuid
import sqlite3
import os
import json

from werkzeug.security import generate_password_hash


def getPathTo(relativePath):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relativePath))

dbPath = getPathTo("../instance/dev.sqlite")

# Mocked Data
usersDataPath = getPathTo("../.data/users.json")
conversationsDataPath = getPathTo("../.data/conversations.json")

db = sqlite3.connect(dbPath)

def create_user(*, id, email, password):
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO users(id, email, password)
            VALUES(?,?,?)
            """, (id, email, password)
            )
        
        cursor.close()
        print(
            f"""
              User {id} created successfully\n
              Details:\n
              - email : {email}
            """
        )
    
    except Exception as e:
        print(str(e))
        if "UNIQUE constraint failed".lower() in str(e).lower() :
            print(f"User with email {email} could not be created")
            pass
        
def create_conversation(*, convData):
    try:
        # convData['conv_id'] = 'CNV-' . uuid.uuid4()
        # convData['message_id'] = 'MSG-' . uuid.uuid4()
        
        
        cursor = db.cursor()
        
        sender_id = cursor.execute('SELECT id from users where email = ?', (convData['sender'],)).fetchone()[0]
        recipient_id = cursor.execute('SELECT id from users where email = ?', (convData['recipient'],)).fetchone()[0]
        print("Sender Id is " + sender_id)
        print("Receiver Id is " + recipient_id)

        cursor.executescript(
            """
            BEGIN
            INSERT INTO conversations(id) VALUES(:conv_id)
            INSERT INTO conversations_members()
            COMMIT
            """, convData
        )
    
    except Exception as e:
        print(str(e))
        pass
    
try:
    # with open(usersDataPath, "r") as f:
    #     arrayOfUsers = json.loads(f.read())
        
    #     for u in arrayOfUsers:
    #         _id = uuid.uuid4()
    #         create_user(
    #             id = str(_id),
    #             email = u['email'],
    #             password = generate_password_hash(u['password']),
    #         )
    # db.commit()
    
    with open(conversationsDataPath, "r") as f:
        conversations = json.loads(f.read())
        
        for c in conversations:
            create_conversation(convData = c)  
    
    print("Seeding users done!")
    
except Exception as e:
    raise e
    print(str(e))
    


