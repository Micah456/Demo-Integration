import unittest
import SYSAPI_OS_ITEM_FUNC as sysItem
import os
import pyodbc
import traceback


class TestServer(unittest.TestCase):
    item1 = {"ID": 1, "Name": "Apple Juice", "Description": "Tasty and refreshing beverage", "Price": 1.5,
             "ImageURL": None}
    item2 = {'Name': 'Orange Juice', 'Description': 'World-class beverage', 'Price': 2.0,
             'ImageURL': None}
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
        print("-------------- TEST: GETTING ITEMS ----------------")
        assert sysItem.get_item() == [self.item1]

    def test_get_item_by_ID(self):
        print("-------------- TEST: GETTING ITEM BY ID ----------------")
        assert sysItem.get_item(self.item1.get('ID')) == self.item1

    def test_post_item(self):
        print("-------------- TEST: CREATING ITEM ----------------")
        self.assertIsNone(sysItem.get_item_by_name(self.item2.get('Name')))
        new_item = sysItem.create_item(self.item2)
        new_item.pop("ID")
        print("-------------CREATED ITEM: ")
        print(new_item)
        assert new_item.get('Name') == self.item2.get('Name')
        assert new_item.get('Description') == self.item2.get('Description')
        assert new_item.get('Price') == self.item2.get('Price')
        assert new_item.get('ImageURL') == self.item2.get('ImageURL')
        self.assertFalse(sysItem.create_item(self.item2))

    def test_get_item_by_name(self):
        print("-------------- TEST: GETTING ITEM BY NAME ----------------")
        assert sysItem.get_item_by_name(self.item1.get('Name')) == self.item1

    def test_put_item_by_id(self):
        print("-------------- TEST: UPDATING ITEM BY ID ----------------")
        new_item = sysItem.create_item(self.item3)
        new_item['Price'] = 0.5
        new_item2 = sysItem.update_item_by_id(new_item.get('ID'), new_item)
        assert new_item2.get('Name') == self.item3.get('Name')
        assert new_item2.get('Description') == self.item3.get('Description')
        assert new_item2.get('Price') == 0.5
        assert new_item2.get('ImageURL') == self.item3.get('ImageURL')
        self.assertIsNone(sysItem.update_item_by_id(-1, new_item2))


# driver code
if __name__ == '__main__':
    unittest.main()
