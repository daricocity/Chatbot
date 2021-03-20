from django.db.models import Q
from rest_framework import serializers
from chats.models import GenericFileUpload
from .models import UserProfile, CustomUser
from chats.serializers import GenericFileUploadSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        exclude = ("password", )

class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only = True)
    user_id = serializers.IntegerField(write_only = True)
    profile_picture = GenericFileUploadSerializer(read_only = True)
    profile_picture_id = serializers.IntegerField(write_only = True, required = False)
    message_count = serializers.SerializerMethodField('get_message_count')
    
    class Meta:
        model = UserProfile
        fields = "__all__"
        
    def get_message_count(self, obj):
        try:
            user_id = self.context['request'].user.id
        except Exception as e:
            user_id = None
        
        from chats.models import Message
        message = Message.objects.filter(
            Q(sender = user_id, receiver = obj.user.id) | Q(sender = obj.user.id, receiver = user_id)
        ).distinct()
        return message.count()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()