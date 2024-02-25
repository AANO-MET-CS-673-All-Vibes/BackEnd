import pymysql

# exists(): this method determines if an account exists or not
# Parameter: email - email associated with this account
# Return: Boolean

def exists(email):
    db = pymysql.connections.Connection(host="127.0.0.1", user="root", password="AllVibes01", database="allvibes")
    cursor = db.cursor()
    
    count = cursor.execute("SELECT * FROM accounts WHERE email=\"" + email + "\"")

    cursor.close()
    db.close()

    if count == 0:
        return False
    else:
        return True
