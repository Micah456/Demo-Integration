import os
import pyodbc
import traceback
from dotenv import load_dotenv

load_dotenv()
server = os.getenv("server")
database = os.getenv("database")
stock_table = os.getenv("stock_table")

conn_str = "Driver=SQL Server;Server=" + server + ";Database=" + database + ";Trusted_Connection=yes;"
columns = ("ID", "Name", "Description", "Price", "ImageURL")


def get_item(id=None):
    '''Returns item dictionary from database by id.
    Returns an array of all stock dictionaries if no id given.
    Returns None if something went wrong.'''
    print("-------------- GETTING ITEM(S) ----------------")
    try:
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        if id:
            statement = "SELECT * FROM " + stock_table + " WHERE ID = " + str(id)
            print(statement)
            cursor.execute(statement)
            print("execution successful")
            data = cursor.fetchall()
            print("-------------- ITEM RETRIEVAL COMLPETE (by id) ----------------")
            return create_item_dict(data[0])
        else:
            statement = "SELECT * FROM " + stock_table
            print(statement)
            cursor.execute(statement)
            data = cursor.fetchall()
            print("execution successful")
            print("-------------- STOCK RETRIEVAL COMPLETE ----------------")
            return collate_item_dicts(data)
    except Exception:
        print("Something went wrong!")
        print(traceback.format_exc())
        return None


def create_item_dict(row):
    '''Generate a item dictionary from the row data returned from the database'''
    print("--------- GENERATING ITEM DICT ------------")
    return {
        "ID": row[0],
        "Name": row[1],
        "Description": row[2],
        "Price": float(row[3]),
        "ImageURL": row[4]
    }


def collate_item_dicts(data):
    '''Create item dict arrays from data returned from the database'''
    stock_array = []
    for row in data:
        stock_array.append(create_item_dict(row))
    return stock_array
