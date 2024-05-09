''' database functions '''
import sqlite3
import hashlib
import datetime

USER_DB_FILE_LOCATION = "database_file/users.db"
NOTE_DB_FILE_LOCATION = "database_file/notes.db"
IMAGE_DB_FILE_LOCATION = "database_file/images.db"

def list_users():
    '''list user'''
    _conn = sqlite3.connect(USER_DB_FILE_LOCATION)
    _c = _conn.cursor()

    _c.execute("SELECT id FROM users;")
    result = [x[0] for x in _c.fetchall()]

    _conn.close()

    return result

def verify(user_id, password):
    '''Verify user'''
    _conn = sqlite3.connect(USER_DB_FILE_LOCATION)
    _c = _conn.cursor()

    # Use parameterized queries to prevent SQL injection
    query = "SELECT pw FROM users WHERE id = ?;"
    _c.execute(query, (user_id,))

    # Securely compare the stored password with the provided password's hash
    result = _c.fetchone()
    if result:
        stored_password = result[0]
        provided_password_hash = hashlib.sha256(password.encode()).hexdigest()
        return stored_password == provided_password_hash
    _conn.close()

    return False

def delete_user_from_db(user_id):
    '''delete user'''
    _conn = sqlite3.connect(USER_DB_FILE_LOCATION)
    _c = _conn.cursor()
    _c.execute("DELETE FROM users WHERE id = ?;", (user_id))
    _conn.commit()
    _conn.close()

    # when we delete a user FROM database USERS,
    # we also need to delete all his or her notes data FROM database NOTES
    _conn = sqlite3.connect(NOTE_DB_FILE_LOCATION)
    _c = _conn.cursor()
    _c.execute("DELETE FROM notes WHERE user = ?;", (user_id))
    _conn.commit()
    _conn.close()

    # when we delete a user FROM database USERS, we also need to
    # [1] delete all his or her images FROM image pool (done in app.py)
    # [2] delete all his or her images records FROM database IMAGES
    _conn = sqlite3.connect(IMAGE_DB_FILE_LOCATION)
    _c = _conn.cursor()
    _c.execute("DELETE FROM images WHERE owner = ?;", (user_id))
    _conn.commit()
    _conn.close()

def add_user(user_id, pw):
    '''add user'''
    _conn = sqlite3.connect(USER_DB_FILE_LOCATION)
    _c = _conn.cursor()

    _c.execute("INSERT INTO users values(?, ?)",\
            (user_id.upper(), hashlib.sha256(pw.encode()).hexdigest()))

    _conn.commit()
    _conn.close()

def read_note_from_db(user_id):
    '''read note from db'''
    _conn = sqlite3.connect(NOTE_DB_FILE_LOCATION)
    _c = _conn.cursor()

    command = "SELECT note_id, timestamp, note FROM notes WHERE user = '" + user_id.upper() + "';"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result

def match_user_id_with_note_id(note_id):
    ''' Given the note id, confirm if the current user 
        is the owner of the note which is being operated.'''
    _conn = sqlite3.connect(NOTE_DB_FILE_LOCATION)
    _c = _conn.cursor()

    command = "SELECT user FROM notes WHERE note_id = '" + note_id + "';"
    _c.execute(command)
    result = _c.fetchone()[0]

    _conn.commit()
    _conn.close()

    return result

def write_note_into_db(user_id, note_to_write):
    '''write note into db'''
    _conn = sqlite3.connect(NOTE_DB_FILE_LOCATION)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    _c.execute("INSERT INTO notes values(?, ?, ?, ?)",\
            (user_id.upper(), current_timestamp, note_to_write,\
            hashlib.sha1((id.upper() + current_timestamp).encode()).hexdigest()))

    _conn.commit()
    _conn.close()

def delete_note_from_db(note_id):
    '''delete note from db'''
    _conn = sqlite3.connect(NOTE_DB_FILE_LOCATION)
    _c = _conn.cursor()

    _c.execute("DELETE FROM notes WHERE note_id = ?;", (note_id))

    _conn.commit()
    _conn.close()

def image_upload_record(uid, owner, image_name, timestamp):
    '''image upload'''
    _conn = sqlite3.connect(IMAGE_DB_FILE_LOCATION)
    _c = _conn.cursor()

    _c.execute("INSERT INTO images VALUES (?, ?, ?, ?)", (uid, owner, image_name, timestamp))

    _conn.commit()
    _conn.close()

def list_images_for_user(owner):
    '''list images from user'''
    _conn = sqlite3.connect(IMAGE_DB_FILE_LOCATION)
    _c = _conn.cursor()

    command = f"SELECT uid, timestamp, name FROM images WHERE owner = '{owner}'"
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result

def match_user_id_with_image_uid(image_uid):
    '''Given the note id, confirm if the current user 
       is the owner of the note which is being operated.'''
    _conn = sqlite3.connect(IMAGE_DB_FILE_LOCATION)
    _c = _conn.cursor()

    command = "SELECT owner FROM images WHERE uid = '" + image_uid + "';"
    _c.execute(command)
    result = _c.fetchone()[0]

    _conn.commit()
    _conn.close()

    return result

def delete_image_from_db(image_uid):
    '''delete image from db'''
    _conn = sqlite3.connect(IMAGE_DB_FILE_LOCATION)
    _c = _conn.cursor()

    _c.execute("DELETE FROM images WHERE uid = ?;", (image_uid))

    _conn.commit()
    _conn.close()







if __name__ == "__main__":
    print(list_users())
