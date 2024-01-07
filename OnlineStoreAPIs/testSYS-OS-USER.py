import unittest, os, SYSAPI_OS_USER as sysUser

class TestServer(unittest.TestCase):

    user1 = {'ID': 2, 'First Name': 'Micah', 'Last Name': 'Chuku', 'Username': 'mchuku', 'Password': 'pass1', 'Email Address': 'mchuku@onlinestore.com', 'DOB': '1998-07-24', 'House NumName': '1', 'Street': 'Generic Street', 'City': 'Generic City', 'Country': 'UK', 'Post Code': 'UK12 G34'}
    user2 = {'First Name': 'Marlee', 'Last Name': 'Vaughn', 'Username': 'mvaughn', 'Password': 'pass2', 'Email Address': 'mvaughn@gmail.com', 'DOB': '2006-03-16', 'House NumName': '2', 'Street': 'Generic Street', 'City': 'Generic City', 'Country': 'UK', 'Post Code': 'UK12 G34'}
    def test_get_users(self):
        assert sysUser.get_users() == [self.user1]
    def test_get_user_by_ID(self):
        assert sysUser.get_users(self.user1.get('ID')) == self.user1
    def test_get_user_by_email(self):
        assert sysUser.get_user_by_email(self.user1.get('Email Address')) == self.user1
    '''def test_create_user(self):
        assert sysUser.get_user_by_email(self.user2.get('Email Address')) == None
        sysUser.create_user(self.user2)
        assert sysUser.get_user_by_email(self.user2.get('Email Address')) == self.user2'''
        #Must delete newly created user before running test
    def test_create_users_from_array(self):
        #TODO - create, find, then delete new users
        pass
    #TODO also to do: update user details, delete user, etc.



# driver code
if __name__ == '__main__':
   
    unittest.main()
