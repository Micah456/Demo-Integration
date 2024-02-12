import unittest
import SYSAPI_OS_USER_FUNC as sysUser
import os
import pyodbc
import traceback


class TestServer(unittest.TestCase):
    user1 = {'ID': 2, 'FirstName': 'Micah', 'LastName': 'Chuku', 'UserName': 'mchuku',
             'Password': 'pass1', 'EmailAddress': 'mchuku@onlinestore.com',
             'DOB': '1998-07-24', 'HouseNumName': '1', 'Street': 'Generic Street',
             'City': 'Generic City', 'Country': 'UK', 'PostCode': 'UK12 G34'}
    user2 = {'FirstName': 'Marlee', 'LastName': 'Vaughn', 'UserName': 'mvaughn',
             'Password': 'pass2', 'EmailAddress': 'mvaughn@gmail.com', 'DOB': '2006-03-16',
             'HouseNumName': '2', 'Street': 'Generic Street', 'City': 'Generic City',
             'Country': 'UK', 'PostCode': 'UK12 G34'}
    user3 = {'FirstName': 'Duane', 'LastName': 'Vaughn', 'UserName': 'dvaughn',
             'Password': 'pass3', 'EmailAddress': 'dvaughn@hotmail.com',
             'DOB': '1998-05-09', 'HouseNumName': '2', 'Street': 'Generic Street',
             'City': 'Generic City', 'Country': 'UK', 'PostCode': 'UK12 G34'}

    @classmethod
    def setUpClass(cls):
        print("---------- TEST CLASS SETUP ---------------")
        email2 = "mvaughn@gmail.com"
        email3 = "dvaughn@hotmail.com"
        try:
            server = os.getenv("server")
            database = os.getenv("database")
            users_table = os.getenv("users_table")
            conn_str = ("Driver=SQL Server;Server=" + server + ";Database=" +
                        database + ";Trusted_Connection=yes;")
            statement = ("DELETE FROM " + users_table + " WHERE EmailAddress = '" +
                         email2 + "' OR EmailAddress = '" +
                         email3 + "'")
            print(statement)
            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor()
            cursor.execute(statement)
            cnxn.commit()
            print("-------------- TEST CLASS SETUP COMPLETE -------------")
        except Exception:
            print(traceback.format_exc)
            print("-------------- TEST CLASS SETUP FAILED ---------------")

    def test_get_users(self):
        print("-------------- TEST: GETTING USERS ----------------")
        assert sysUser.get_users() == [self.user1]

    def test_get_user_by_ID(self):
        print("-------------- TEST: GETTING USER BY ID ----------------")
        assert sysUser.get_users(self.user1.get('ID')) == self.user1

    def test_get_user_by_email(self):
        print("-------------- TEST: GETTING USER BY EMAIL ----------------")
        assert sysUser.get_user_by_email(self.user1.get('EmailAddress')) == self.user1

    def test_create_user(self):
        print("-------------- TEST: CREATING USER ----------------")
        self.assertIsNone(sysUser.get_user_by_email(self.user2.get('EmailAddress')))
        new_user = sysUser.create_user(self.user2)
        sysUser.delete_user_by_id(new_user.get('ID'))
        new_user.pop("ID")
        assert new_user == self.user2

    def test_create_users_from_array(self):
        print("-------------- TEST: CREATING USER(S) ----------------")
        user_array = [self.user2, self.user3]
        total_users = len(sysUser.get_users())
        self.assertIsNone(sysUser.get_user_by_email(self.user2.get('EmailAddress')))
        self.assertIsNone(sysUser.get_user_by_email(self.user3.get('EmailAddress')))
        created_users_array = sysUser.create_users_from_array(user_array)
        created_users_array[0].pop('ID')
        created_users_array[1].pop('ID')
        assert created_users_array == user_array
        assert len(sysUser.get_users()) == total_users + 2
        sysUser.delete_user_by_id(sysUser.get_user_id(self.user2.get('EmailAddress')))
        sysUser.delete_user_by_id(sysUser.get_user_id(self.user3.get('EmailAddress')))

    def test_delete_user(self):
        print("-------------- TEST: DELETING USER(S) ----------------")
        self.assertIsNone(sysUser.get_user_by_email(self.user2.get('EmailAddress')))
        total_users = len(sysUser.get_users())
        sysUser.create_user(self.user2)
        assert len(sysUser.get_users()) == total_users + 1
        user_data = sysUser.get_user_by_email(self.user2.get('EmailAddress'))
        self.assertTrue(sysUser.delete_user_by_id(user_data.get('ID')))
        assert len(sysUser.get_users()) == total_users
        self.assertIsNone(sysUser.get_users(user_data.get('ID')))

    def test_update_user(self):
        print("-------------- TEST: UPDATING USER ----------------")
        user_data = sysUser.create_user(self.user2)
        assert user_data.get('DOB') == self.user2.get('DOB')
        user_data['DOB'] = '1998-05-10'
        self.assertTrue(sysUser.update_user_by_id(user_data.get('ID'), user_data))
        user_data = sysUser.get_user_by_email(self.user2.get('EmailAddress'))
        assert user_data.get('DOB') == '1998-05-10'
        sysUser.delete_user_by_id(sysUser.get_user_id(self.user2.get('EmailAddress')))

    def test_get_user_ID(self):
        print("-------------- TEST: GETTING USER ID ----------------")
        assert sysUser.get_user_id(self.user1.get('EmailAddress')) == 2


# driver code
if __name__ == '__main__':
    unittest.main()
