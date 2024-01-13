import unittest, os, SYSAPI_OS_USER as sysUser

class TestServer(unittest.TestCase):

    user1 = {'ID': 2, 'First Name': 'Micah', 'Last Name': 'Chuku', 'Username': 'mchuku', 'Password': 'pass1', 'Email Address': 'mchuku@onlinestore.com', 'DOB': '1998-07-24', 'House NumName': '1', 'Street': 'Generic Street', 'City': 'Generic City', 'Country': 'UK', 'Post Code': 'UK12 G34'}
    user2 = {'First Name': 'Marlee', 'Last Name': 'Vaughn', 'Username': 'mvaughn', 'Password': 'pass2', 'Email Address': 'mvaughn@gmail.com', 'DOB': '2006-03-16', 'House NumName': '2', 'Street': 'Generic Street', 'City': 'Generic City', 'Country': 'UK', 'Post Code': 'UK12 G34'}
    user3 = {'First Name': 'Duane', 'Last Name': 'Vaughn', 'Username': 'dvaughn', 'Password': 'pass3', 'Email Address': 'dvaughn@hotmail.com', 'DOB': '1998-05-09', 'House NumName': '2', 'Street': 'Generic Street', 'City': 'Generic City', 'Country': 'UK', 'Post Code': 'UK12 G34'}
    def test_get_users(self):
        assert sysUser.get_users() == [self.user1]

    def test_get_user_by_ID(self):
        assert sysUser.get_users(self.user1.get('ID')) == self.user1

    def test_get_user_by_email(self):
        assert sysUser.get_user_by_email(self.user1.get('Email Address')) == self.user1

    def test_create_user(self):
        assert sysUser.get_user_by_email(self.user2.get('Email Address')) == None
        sysUser.create_user(self.user2)
        found_user = sysUser.get_user_by_email(self.user2.get('Email Address'))
        sysUser.delete_user_by_id(found_user.get('ID'))
        found_user.pop("ID")
        assert found_user == self.user2
        
    def test_create_users_from_array(self):
        #TODO - create, find, then delete new users
        user_array = [self.user2, self.user3]
        total_users = len(sysUser.get_users())
        assert sysUser.get_user_by_email(self.user2.get('Email Address')) == None
        assert sysUser.get_user_by_email(self.user3.get('Email Address')) == None
        sysUser.create_users_from_array(user_array)
        assert len(sysUser.get_users()) == total_users + 2
        found_user1 = sysUser.get_user_by_email(self.user2.get('Email Address'))
        found_user2 = sysUser.get_user_by_email(self.user3.get('Email Address'))
        sysUser.delete_user_by_id(found_user1.get('ID'))
        sysUser.delete_user_by_id(found_user2.get('ID'))
        
    def test_delete_user(self):
        assert sysUser.get_user_by_email(self.user2.get('Email Address')) == None
        total_users = len(sysUser.get_users())
        sysUser.create_user(self.user2)
        assert len(sysUser.get_users()) == total_users + 1
        user_data = sysUser.get_user_by_email(self.user2.get('Email Address'))
        assert sysUser.delete_user_by_id(user_data.get('ID')) == True
        assert len(sysUser.get_users()) == total_users
        assert sysUser.get_users(user_data.get('ID')) == None

    #TODO also to do: update user details
    def test_update_user(self):
        pass



# driver code
if __name__ == '__main__':
   
    unittest.main()
