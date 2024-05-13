from .models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # These are claims, you can add custom claims
        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.profile.bio
        token['image'] = str(user.profile.image)
        
        # ...
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']

        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    
class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ['id', 'user', 'title', 'completed']    

class BlogSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Blogs
        fields = ['id', 'user', 'title', 'content', 'date', 'likes','views']     


class BlogViewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Blogs
        fields = ['id', 'user', 'title', 'content', 'date', 'likes','views']    

class MemeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Meme
        fields = ['id', 'user', 'description', 'date', 'images', 'likes']    

class CodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CodeSnippet
        fields = ['code_id', 'title', 'code', 'content', 'topic']  

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'language']  

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['id','topic']        


class TutorialNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialName
        fields = ['id', 'tutorialName', 'tutorialContent', 'tutorialImage']  


class TutorialPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialPost
        fields = ['post_id', 'post_title', 'post_content', 'post_file', 'tutorialName', 'post_video']  

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['blog', 'user', 'date', 'content']      

class TutorialCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment_tutorials
        fields = ['post', 'user', 'date', 'content']    

class CommentGetTutSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment_tutorials
        fields = ['post', 'user', 'date', 'content']          

class CommentGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ['blog', 'user', 'date', 'content']      

class ContactSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']     

class ProblemSolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem_solve
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'