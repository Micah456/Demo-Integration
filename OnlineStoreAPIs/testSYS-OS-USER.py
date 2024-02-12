import unittest, os, SYSAPI_OS_USER_FUNC as sysUser

class TestServer(unittest.TestCase):

    user1 = {'ID': 2, 'FirstName': 'Micah', 'LastName': 'Chuku', 'UserName': 'mchuku', 'Password': 'pass1', 'EmailAddress': 'mchuku@onlinestore.com', 'DOB': '1998-07-24', 'HouseNumName': '1', 'Street': 'Generic Street', 'City': 'Generic City', 'Country': 'UK', 'PostCode': 'UK12 G34'}
    user2 = {'FirstName': 'Marlee', 'LastName': 'Vaughn', 'UserName': 'mvaughn', 'Password': 'pass2', 'EmailAddress': 'mvaughn@gmail.com', 'DOB': '2006-03-16', 'HouseNumName': '2', 'Street': 'Generic Street', 'City': 'Generic City', 'Country': 'UK', 'PostCode': 'UK12 G34'}
    user3 = {'FirstName': 'Duane', 'LastName': 'Vaughn', 'UserName': 'dvaughn', 'Password': 'pass3', 'EmailAddress': 'dvaughn@hotmail.com', 'DOB': '1998-05-09', 'HouseNumName': '2', 'Street': 'Generic Street', 'City': 'Generic City', 'Country': 'UK', 'PostCode': 'UK12 G34'}
    def test_get_users(self):
        assert sysUser.get_users() == [self.user1]

    def test_get_user_by_ID(self):
        assert sysUser.get_users(self.user1.get('ID')) == self.user1

    def test_get_user_by_email(self):
        assert sysUser.get_user_by_email(self.user1.get('EmailAddress')) == self.user1

    def test_create_user(self):
        assert sysUser.get_user_by_email(self.user2.get('EmailAddress')) == None
        new_user = sysUser.create_user(self.user2)
        sysUser.delete_user_by_id(new_user.get('ID'))
        new_user.pop("ID")
        assert new_user == self.user2
        
    def test_create_users_from_array(self):
        #TODO - create, find, then delete new users
        user_array = [self.user2, self.user3]
        total_users = len(sysUser.get_users())
        assert sysUser.get_user_by_email(self.user2.get('EmailAddress')) == None
        assert sysUser.get_user_by_email(self.user3.get('EmailAddress')) == None
        created_users_array = sysUser.create_users_from_array(user_array)
        created_users_array[0].pop('ID')
        created_users_array[1].pop('ID')
        assert created_users_array == user_array
        assert len(sysUser.get_users()) == total_users + 2

        sysUser.delete_user_by_id(sysUser.get_user_id(self.user2.get('EmailAddress')))
        sysUser.delete_user_by_id(sysUser.get_user_id(self.user3.get('EmailAddress')))
        
    def test_delete_user(self):
        assert sysUser.get_user_by_email(self.user2.get('EmailAddress')) == None
        total_users = len(sysUser.get_users())
        sysUser.create_user(self.user2)
        assert len(sysUser.get_users()) == total_users + 1
        user_data = sysUser.get_user_by_email(self.user2.get('EmailAddress'))
        assert sysUser.delete_user_by_id(user_data.get('ID')) == True
        assert len(sysUser.get_users()) == total_users
        assert sysUser.get_users(user_data.get('ID')) == None

    #TODO also to do: update user details
    def test_update_user(self):
        user_data = sysUser.create_user(self.user2)
        assert user_data.get('DOB') == self.user2.get('DOB')
        user_data['DOB'] = '1998-05-10'
        assert sysUser.update_user_by_id(user_data.get('ID'), user_data) == True
        user_data = sysUser.get_user_by_email(self.user2.get('EmailAddress'))
        assert user_data.get('DOB') == '1998-05-10'
        sysUser.delete_user_by_id(sysUser.get_user_id(self.user2.get('EmailAddress')))

    def test_get_user_ID(self):
        assert sysUser.get_user_id(self.user1.get('EmailAddress')) == 2




# driver code
if __name__ == '__main__':
   
    unittest.main()
