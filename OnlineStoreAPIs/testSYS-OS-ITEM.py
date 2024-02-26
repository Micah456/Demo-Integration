import unittest
import SYSAPI_OS_ITEM_FUNC as sysItem
import os
import pyodbc
import traceback


class TestServer(unittest.TestCase):
    item1 = {"ID": 1, "Name": "Apple Juice", "Description": "Tasty and refreshing beverage", "Price": 1.5,
             "ImageURL": None}
    item2 = {"Name": "Orange Juice", "Description": "World-class beverage", "Price": 2.0,
             "ImageURL": None}
    item3 = {"Name": "Tomato Juice", "Description": "Why is this even a thing?", "Price": 1.75,
             "ImageURL": None}

    @classmethod
    def setUpClass(cls):
        print("---------- TEST CLASS SETUP ---------------")
        item_name_2 = "Orange Juice"
        item_name_3 = "Tomato Juice"
        try:
            server = os.getenv("server")
            database = os.getenv("database")
            stock_table = os.getenv("stock_table")
            conn_str = ("Driver=SQL Server;Server=" + server + ";Database=" +
                        database + ";Trusted_Connection=yes;")
            statement = ("DELETE FROM " + stock_table + " WHERE Name = '" +
                         item_name_2 + "' OR Name = '" +
                         item_name_3 + "'")
            print(statement)
            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor()
            cursor.execute(statement)
            cnxn.commit()
            print("-------------- TEST CLASS SETUP COMPLETE -------------")
        except Exception:
            print(traceback.format_exc)
            print("-------------- TEST CLASS SETUP FAILED ---------------")

    def test_get_stock(self):
        print("-------------- TEST: GETTING USERS ----------------")
        assert sysItem.get_item() == [self.item1]

    def test_get_item_by_ID(self):
        print("-------------- TEST: GETTING USER BY ID ----------------")
        assert sysItem.get_item(self.item1.get('ID')) == self.item1


# driver code
if __name__ == '__main__':
    unittest.main()
