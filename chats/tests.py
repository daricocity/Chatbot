from PIL import Image
from six import BytesIO
from rest_framework.test import APITestCase
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)

class TestFileUpload(APITestCase):
    file_upload_url = "/message/file-upload"

    def test_file_upload(self):
        # definition
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front1.png', avatar.getvalue())
        data = {
            "file_upload": avatar_file
        }

        # processing
        response = self.client.post(self.file_upload_url, data = data)
        result = response.json()

        # assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["id"], 1)
        
class TestMessage(APITestCase):
    login_url = '/account/login'
    message_url = "/message/message"
    
    def setUp(self):
        from accounts.models import CustomUser, UserProfile
        
        payload = {
            "username": "sender",
            "password": "sender123",
            "email": "daricocity@gmail.com"
        }
        
        # sender
        self.sender = CustomUser.objects._create_user(**payload)
        UserProfile.objects.create(first_name = 'sender', last_name = 'sender', user = self.sender, caption = 'sender', about = 'sender')
        
        # login
        response = self.client.post(self.login_url, data = payload)
        result = response.json()
        
        self.bearer = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(result['access'])
        }
        
        # receiver
        self.receiver = CustomUser.objects._create_user('receiver', 'receiver123', email = 'darl123@gmail.com')
        UserProfile.objects.create(first_name = 'receiver', last_name = 'receiver', user = self.receiver, caption = 'receiver', about = 'receiver')
        
        # authenticate
        # self.client.force_authenticate(user = self.sender)
        
    def test_post_message(self):
        
        payload = {
            'sender_id': self.sender.id,
            'receiver_id': self.receiver.id,
            'message': 'test message'
        }
        
        # processing
        response = self.client.post(self.message_url, data = payload, **self.bearer)
        result = response.json()
        # print(result)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], 'test message')
        self.assertEqual(result['sender']['user']['username'], 'sender')
        self.assertEqual(result['receiver']['user']['username'], 'receiver')
        
    def test_get_message(self):
        response = self.client.get(self.message_url+f"?user_id={self.receiver.id}", **self.bearer)
        result = response.json()
        
        self.assertEqual(response.status_code, 200)

    def test_update_message(self):

        # create message
        payload = {
            "sender_id": self.sender.id,
            "receiver_id": self.receiver.id,
            "message": "test message",

        }
        self.client.post(self.message_url, data=payload, **self.bearer)

        # update message
        payload = {
            "message": "test message updated",
            "is_read": True
        }
        response = self.client.patch(self.message_url+"/1", data=payload, **self.bearer)
        result = response.json()

        # assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["message"], "test message updated")
        self.assertEqual(result["is_read"], True)
