from django.test import TestCase
from .models import CustomUser, UserProfile
from rest_framework.test import APITestCase
from chats.tests import create_image, SimpleUploadedFile
from .views import get_random, get_access_token, get_refresh_token

# Create your tests here.
class TestUserInfo(APITestCase):
    login_url = '/account/login'
    profile_url = '/account/profile'
    file_upload_url = "/message/file-upload"
    
    def setUp(self):
        
        payload = {
            "username": "admin",
            "password": "123456",
            "email": "daricocity@gmail.com"
        }
        
        self.user = CustomUser.objects._create_user(**payload)
        # self.client.force_authenticate(user = self.user)
        
        # login
        response = self.client.post(self.login_url, data = payload)
        result = response.json()
        
        self.bearer = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(result['access'])
        }
        
    def test_post_user_profile(self):
    
        payload = {
            "user_id": self.user.id,
            "first_name": "John",
            "last_name": "Kennedy",
            "caption": "Being alive is different from living",
            "about": "I am a passionation lover of ART, graphics and creation"
        }
        
        response = self.client.post(self.profile_url, data = payload, **self.bearer)
        result = response.json()
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "John")
        self.assertEqual(result["last_name"], "Kennedy")
        self.assertEqual(result["user"]["username"], "admin")
        
    def test_post_user_profile_with_profile_picture(self):
        
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front1.png', avatar.getvalue())
        data = {
            "file_upload": avatar_file
        }

        # processing
        response = self.client.post(self.file_upload_url, data=data, **self.bearer)
        result = response.json()
        
        payload = {
            "user_id": self.user.id,
            "first_name": "John",
            "last_name": "Kennedy",
            "caption": "Being alive is different from living",
            "about": "I am a passionation lover of ART, graphics and creation",
            "profile_picture_id": result["id"]
        }
        
        response = self.client.post(self.profile_url, data = payload, **self.bearer)
        result = response.json()
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "John")
        self.assertEqual(result["last_name"], "Kennedy")
        self.assertEqual(result["user"]["username"], "admin")
        self.assertEqual(result["profile_picture"]["id"], 1)
        
    def test_update_user_profile(self):
        
        payload = {
            "user_id": self.user.id,
            "first_name": "John",
            "last_name": "Kennedy",
            "caption": "Being alive is different from living",
            "about": "I am a passionation lover of ART, graphics and creation"
        }
        
        response = self.client.post(self.profile_url, data = payload, **self.bearer)
        result = response.json()
        
        payload = {
            "first_name": "Adeori",
            "last_name": "Okin",
        }
        
        response = self.client.patch(self.profile_url + f"/{result['id']}", data = payload, **self.bearer)
        result = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["first_name"], "Adeori")
        self.assertEqual(result["last_name"], "Okin")
        self.assertEqual(result["user"]["username"], "admin")
        
    def test_user_search(self):
        
        UserProfile.objects.create(user = self.user, first_name = 'Adefemi', last_name = 'Oseni', caption = 'I am still breathing', about = 'I am a developer')
        
        user2 = CustomUser.objects._create_user(username = 'tester', password = 'tester123', email = 'tester@gmail.com')
        UserProfile.objects.create(user = user2, first_name = 'Olu', last_name = 'Shola', caption = 'I am alive', about = 'I am a developer')
        
        user3 = CustomUser.objects._create_user(username = 'dreyman', password = 'drey123', email = 'user3@gmail.com')
        UserProfile.objects.create(user = user3, first_name = 'Adeyemi', last_name = 'Shola', caption = 'I am alive', about = 'I am a developer')
        
        # test keyword for Adefemi
        url = self.profile_url + '?keyword=oseni'
        
        response = self.client.get(url, **self.bearer)
        result = response.json()['results']
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 0)
        # self.assertEqual(result[0]['user']['username'], 'admin')
        # self.assertEqual(result[0]['message_count'], 0)
        
        # test keyword for Ade
        url = self.profile_url + '?keyword=ade'
        
        response = self.client.get(url, **self.bearer)
        result = response.json()['results']
        print(result)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)
        # self.assertEqual(result[0]['user']['username'], 'admin')
    
class TestAuth(APITestCase):
    login_url = '/account/login'
    refresh_url = '/account/refresh'
    register_url = '/account/register'
    
    def test_register(self):
        payload = {
            "username": "Admin",
            "password": "123456",
            "email": "daricocity@gmail.com"
        }
        
        # regiter
        response = self.client.post(self.register_url, data = payload)
        
        # check that we obtain a status of 201
        self.assertEqual(response.status_code, 201)
        
    def test_login(self):
        payload = {
            "username": "Admin",
            "password": "123456",
            "email": "daricocity@gmail.com"
        }
        
        # register
        self.client.post(self.register_url, data = payload)
        
        # login
        response = self.client.post(self.login_url, data = payload)
        result = response.json()
        
        # check that we obtain a status of 200
        self.assertEqual(response.status_code, 200)
        
        # check that we obtain both the refresh and access token
        self.assertTrue(result['access'])
        self.assertTrue(result['refresh'])
        
    def test_refresh(self):
        payload = {
            "username": "Admin",
            "password": "123456",
            "email": "daricocity@gmail.com"
        }
        
        # register
        self.client.post(self.register_url, data = payload)
        
        # login
        response = self.client.post(self.login_url, data = payload)
        refresh = response.json()['refresh']
        
        # get refresh
        response = self.client.post(self.refresh_url, data = {"refresh": refresh})
        result = response.json()
        
        # check that we obtain a status of 200
        self.assertEqual(response.status_code, 200)
        
        # check that we obtain both the refresh and access token
        self.assertTrue(result['access'])
        self.assertTrue(result['refresh'])
        
class TestGenericFunctions(APITestCase):
    
    def test_get_random(self):
        rand1 = get_random(10)
        rand2 = get_random(10)
        rand3 = get_random(15)
        
        # check that we are getting result
        self.assertTrue(rand1)
        
        # check that rand1 is not equal to rand2
        self.assertNotEqual(rand1, rand2)
        
        # check that the length of result is what is expected
        self.assertEqual(len(rand1), 10)
        self.assertEqual(len(rand3), 15)
        
    def test_get_access_token(self):
        payload = {'id': 1}
        token = get_access_token(payload)
        
        # check that we are getting result
        self.assertTrue(token)
        
    def test_get_refresh_token(self):
        payload = {'id': 1}
        token = get_refresh_token()
        
        # check that we are getting result
        self.assertTrue(token)
        
