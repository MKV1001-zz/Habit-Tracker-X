from email import message
import sqlite3
from passlib.context import CryptContext


conn = sqlite3.connect("hyve.db")

##hashing settings 
pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

def table_init():
    conn.execute(
        """
        CREATE TABLE USERS(
            ID INT PRIMARY KEY,
            USERNAME TEXT,
            PASSWORD_HASH TEXT
        );
        """
    )
    conn.close()
def signup(username,password):
    password = password.upper()
    password_hash = pwd_context.hash(password)
    params = (username,password_hash)
    conn.execute(f"""
        INSERT INTO USERS(USERNAME,PASSWORD_HASH)
        VALUES (?,?)
    """,params)
    conn.commit()
    conn.close()


def login(username,password):
    cursor = conn.execute("SELECT PASSWORD_HASH FROM USERS where USERNAME=?",(username,))
    password = password.upper()
    rows = cursor.fetchall()
    if len(rows)!=0: 
       password_hash = rows[0][0]
       if pwd_context.verify(password,password_hash):
           return {'status':True, 'message':"verified"}
       else:
            return {'status':False, 'message':"Wrong Password"}
    else:
        return {'status':False, 'message':"No such User"}
         
print(login('m1','vemms2001'))