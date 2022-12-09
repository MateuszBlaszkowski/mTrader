import os
import db
try:
    file = open("login_temp.txt", "r")

    computer_id = file.readline()
    login = file.readline()
    file.close()
    computer_id = int(computer_id)
    db.cursor.execute(f"SELECT user_login FROM remembered_users WHERE computer_id = {computer_id}")
    result = db.cursor.fetchone()
    if result[0] == login:
        import main
        main.f1(login)
except:
    os.system('python login.py')
