import os, json, pyodbc
from dotenv import load_dotenv

load_dotenv()
server = os.getenv("server")
database = os.getenv("database")
users_table = os.getenv("users_table")

conn_str = "Driver=SQL Server;Server=" + server + ";Database=" + database + ";Trusted_Connection=yes;"

def create_user_dict(row):
    return {
        "ID": row[0],
        "First Name": row[1],
        "Last Name": row[2],
        "Username": row[3],
        "Password": row[4],
        "Email Address": row[5],
        "DOB": row[6],
        "House NumName": row[7],
        "Street": row[8],
        "City": row[9],
        "Country": row[10],
        "Post Code": row[11]
    }

def collate_user_dicts(data):
    users_array = []
    for row in data:
        users_array.append(create_user_dict(row))
    return users_array

def get_users(id=None):
    try:
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        if(id):
            statement = "SELECT * FROM " + users_table + " WHERE ID = " + str(id)
            print(statement)
            cursor.execute(statement)
            print("execution successful")
            data = cursor.fetchall()
            #return json.dumps(create_user_dict(data[0]))
            return create_user_dict(data[0])
        else:
            statement = "SELECT * FROM " + users_table
            print(statement)
            cursor.execute(statement)
            data = cursor.fetchall()
            print("execution successful")
            #return json.dumps(collate_user_dicts(data))
            return collate_user_dicts(data)
    except Exception as e:
        print("Something went wrong!")
        print(e)
        return None
    
def get_user_by_email(email):
    try:
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        statement = "SELECT * FROM " + users_table + "WHERE 'Email Address' = " + email
        print(statement)
        cursor.execute(statement)
        data = cursor.fetchall()
        print("execution successful")
        return create_user_dict(data[0])
    except Exception as e:
        print("Something went wrong!")
        print(e)
        return None

def create_user(user_dict):
    try:
        values = str(list(user_dict.values()))
        statement = "INSERT INTO " + users_table + "([FirstName], [LastName], [UserName], [Password], [EmailAddress], [DOB], [HouseNumName], [Street], [City], [Country], [PostCode]) VALUES (" + values[1:len(values)-1] + ")"
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        cursor.execute(statement)
        cnxn.commit()
        return True
    except Exception as e:
        print(e)
        print("Error: could not add user")
        return False


def create_users_from_array(user_dict_array):
    for user_dict in user_dict_array:
        create_user(user_dict)

if __name__ == '__main__':
    #print("Get all users:")
    #print(get_users())
    #print("Get user id 2")
    #print(get_users(2))
    #print("create user")
    #user1 = {'First Name': 'Micah', 'Last Name': 'Chuku', 'Username': 'mchuku', 'Password': 'pass1', 'Email Address': 'mchuku@onlinestore.com', 'DOB': '1998-07-24', 'House NumName': '1', 'Street': 'Generic Street', 'City': 'Generic City', 'Country': 'UK', 'Post Code': 'UK12 G34'}
    #print(create_user(user1))