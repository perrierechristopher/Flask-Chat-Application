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
        convData['conv_id'] = 'CNV-' + str(uuid.uuid4())
        convData['message_id'] = 'MSG-' + str(uuid.uuid4())
        
        cursor = db.cursor()
        
        convData['sender_id'] = cursor.execute('SELECT id from users where email = ?', (convData['sender'],)).fetchone()[0]
        convData['recipient_id'] = cursor.execute('SELECT id from users where email = ?', (convData['recipient'],)).fetchone()[0]

        cursor.execute(
            "INSERT INTO conversations(id) VALUES(:conv_id)",
            convData
        )
        
        cursor.execute(
            "INSERT INTO conversation_members(user_id, conversation_id) VALUES (:sender_id, :conv_id), (:recipient_id, :conv_id)",
            convData
        )
                
        cursor.execute(
            "INSERT INTO messages(id, conversation_id, sender_id, content) VALUES (:message_id, :conv_id, :sender_id, :content)",
            convData
        )
        
        db.commit()
    
    except Exception as e:
        print(str(e))
    
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
    


