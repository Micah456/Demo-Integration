import os
import pyodbc
import traceback
from dotenv import load_dotenv

load_dotenv()
server = os.getenv("server")
database = os.getenv("database")
users_table = os.getenv("users_table")

conn_str = "Driver=SQL Server;Server=" + server + ";Database=" + database + ";Trusted_Connection=yes;"
columns = ("ID", "FirstName", "LastName", "UserName", "Password", "EmailAddress",
           "DOB", "HouseNumName", "Street", "City", "Country", "PostCode")


def create_user_dict(row):
    '''Generate a user dictionary from the row data returned from the database'''
    print("--------- Generating user dict ------------")
    return {
        "ID": row[0],
        "FirstName": row[1],
        "LastName": row[2],
        "UserName": row[3],
        "Password": row[4],
        "EmailAddress": row[5],
        "DOB": row[6],
        "HouseNumName": row[7],
        "Street": row[8],
        "City": row[9],
        "Country": row[10],
        "PostCode": row[11]
    }


def collate_user_dicts(data):
    '''Create an user dictionary array from data returned from the database'''
    users_array = []
    for row in data:
        users_array.append(create_user_dict(row))
    return users_array


def get_users(id=None):
    '''Returns user dictionary from database by id.
    Returns an array of all user dictionaries if no id given.
    Returns None if something went wrong.'''
    print("-------------- GETTING USER(S) ----------------")
    try:
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        if id:
            statement = "SELECT * FROM " + users_table + " WHERE ID = " + str(id)
            print(statement)
            cursor.execute(statement)
            print("execution successful")
            data = cursor.fetchall()
            print("-------------- USER RETRIEVAL COMLPETE (by id) ----------------")
            return create_user_dict(data[0])
        else:
            statement = "SELECT * FROM " + users_table
            print(statement)
            cursor.execute(statement)
            data = cursor.fetchall()
            print("execution successful")
            print("-------------- USER(S) RETRIEVAL COMPLETE ----------------")
            return collate_user_dicts(data)
    except Exception:
        print("Something went wrong!")
        print(traceback.format_exc())
        return None


def get_user_by_email(email):
    '''Returns user dictionary based on email address.
    Returns None if none found'''
    print("-------- GETTING USER BY EMAIL ------------")
    try:
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        statement = "SELECT * FROM " + users_table + " WHERE EmailAddress = '" + email + "'"
        print(statement)
        cursor.execute(statement)
        data = cursor.fetchall()
        print("execution successful")
        print("-------------- USER RETRIEVAL COMPLETE (by email) ----------------")
        print("data: ")
        print(data[0])
        return create_user_dict(data[0])
    except Exception:
        print("--------- GET USER BY EMAIL: Something went wrong! -------------")
        print(traceback.format_exc())
        return None


def create_user(user_dict):
    '''Adds a user to the database using data from a user dictionary.
    If successful, returns the user just created as a dictionary, else returns False.'''
    print("---------- CREATING USER -------------")
    try:
        values = str(list(user_dict.values()))
        statement = ("INSERT INTO " + users_table + "([FirstName], [LastName], [UserName], " +
                     "[Password], [EmailAddress], [DOB], [HouseNumName], [Street]," +
                     " [City], [Country], [PostCode]) VALUES (" + values[1:len(values)-1] + ")")
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        cursor.execute(statement)
        cnxn.commit()
        print("-------------- USER CREATED ----------------")
        return get_user_by_email(user_dict.get('EmailAddress'))
    except Exception:
        print(traceback.format_exc())
        print("Error: could not add user")
        return False


def create_users_from_array(user_dict_array):
    '''Creates users in the database based on data from an array of user dictionaries.
    Returns array of created users in dictionary form with IDs'''
    print("-------- CREATING USERS FROM ARRAY ------------")
    created_user_array = []
    for user_dict in user_dict_array:
        new_user = create_user(user_dict)
        if new_user:
            created_user_array.append(new_user)
    print("-------------- USER(S) CREATED ----------------")
    return created_user_array


def delete_user_by_id(id):
    '''Deletes a user from the database using the user id.
    Returns true if user deleted. False if not or user doesn't exist.'''
    print("-------- DELETING USER BY ID ------------")
    try:
        if not get_users(id):
            print("Error: user not found.")
            return False
        statement = "DELETE FROM " + users_table + " WHERE ID = " + str(id)
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        cursor.execute(statement)
        cnxn.commit()
        print("-------------- USER DELETED ----------------")
        return True
    except Exception:
        print(traceback.format_exc())
        print("Error: could not delete user.")
        return False


def format_value(val):
    if type(val) is str:
        val = val.replace("'", "''")
        val = "'" + val + "'"
    else:
        if type(val) is bool:
            val = int(val)
        val = str(val)
    return val


def stringify_user_data(user_dict):
    keys = list(user_dict.keys())
    user_string = ""
    for i in range(len(user_dict)):
        if i != 0:
            user_string += ", "
        user_string += "[" + keys[i] + "]" + " = " + format_value(user_dict[keys[i]])
    return user_string


def update_user_by_id(id, user_dict):
    '''Updates user with the corresponding ID to the data passed in the user_dict dictionary.
    Returns True if successful. False if not.'''
    try:
        print("--------- UPDATE USER BY ID ----------------")
        user_dict.pop('ID')
        statement = ("UPDATE " + users_table + " SET " + stringify_user_data(user_dict) +
                     " WHERE ID = " + str(id))
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        cursor.execute(statement)
        cnxn.commit()
        print("----------- USER UPDATED -------------")
        return True
    except Exception:
        print(traceback.format_exc())
        print("Error: could not update user")
        return False


def get_user_id(email):
    '''Returns the ID for the user with the given email address.
    If no user is found or an error occurs, it will return -1'''
    try:
        user_dict = get_user_by_email(email)
        return user_dict.get('ID')
    except Exception:
        print(traceback.format_exc())
        print("Error: could not retrieve user ID")
        return -1


if __name__ == '__main__':
    print("Should not be running as main")
