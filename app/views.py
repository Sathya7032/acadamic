from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .serializer import *
from rest_framework.decorators import api_view, APIView 
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = '/api/reset/done/'


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# Get All Routes

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)


#To do list View
class TodoListView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        todo = Todo.objects.filter(user=user)
        print(user) 
        return todo
        

#To do delete retrive and upadate view
class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        todo_id = self.kwargs['todo_id']

        user = User.objects.get(id=user_id)
        todo = Todo.objects.get(id=todo_id, user=user)

        return todo
    
#To do mark complete
class TodoMarkAsCompleted(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        todo_id = self.kwargs['todo_id']

        user = User.objects.get(id=user_id)
        todo = Todo.objects.get(id=todo_id, user=user)

        todo.completed = True
        todo.save()

        return todo    

#stats todo
    
class TodoSummaryView(APIView):
    def get(self, request, user_id):
        total_tasks = Todo.objects.filter(user_id=user_id).count()
        active_tasks = Todo.objects.filter(user_id=user_id, completed=False).count()
        completed_tasks = Todo.objects.filter(user_id=user_id, completed=True).count()

        return Response({
            'total_tasks': total_tasks,
            'active_tasks': active_tasks,
            'completed_tasks': completed_tasks
        })
    
class BlogListPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 10


class BlogList(ListAPIView):
    queryset = Blogs.objects.all().order_by('-date')
    serializer_class = BlogViewSerializer
    pagination_class = BlogListPagination

class BlogList1(ListAPIView):
    queryset = Blogs.objects.all().order_by('-date')[:6]
    serializer_class = BlogViewSerializer
    

class IncrementViewCountMixin:
    def increment_view_count(self, instance):
        instance.views += 1
        instance.save()

class BlogView(IncrementViewCountMixin, generics.ListAPIView):
    queryset = Blogs.objects.all()
    serializer_class = BlogViewSerializer

    def get_queryset(self):
        blogs_id = self.kwargs['pk']
        post = Blogs.objects.filter(id=blogs_id)
        return post


    

#meme
class MemeList(generics.ListAPIView):
    queryset = Meme.objects.all()
    serializer_class = MemeSerializer  


#Language
class LanguageList(generics.ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer  



class TopicsView(generics.ListAPIView):
     queryset = Topics.objects.all()
     serializer_class = TopicSerializer

     def get_queryset(self):
        language_id = self.kwargs['pk']
        
        code = Topics.objects.filter(language_id=language_id)
        return code


    
#List of each Tutorial Topics
class CodeView(generics.ListAPIView):
    queryset = CodeSnippet.objects.all()
    serializer_class = CodeSerializer

    def get_queryset(self):
        topic_id = self.kwargs['pk']
        
        code = CodeSnippet.objects.filter(topic_id=topic_id)
        return code

#List of Post view
class CodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CodeSnippet.objects.all()
    serializer_class = CodeSerializer 

#Tutorials list view
class TutorialList(generics.ListCreateAPIView):
    queryset = TutorialName.objects.all()
    serializer_class = TutorialNameSerializer


#Each Tutorial view
class TutorialDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TutorialName.objects.all()
    serializer_class = TutorialNameSerializer
    
#List of each Tutorial Topics
class PostView(generics.ListAPIView):
    queryset = TutorialPost.objects.all()
    serializer_class = TutorialPostSerializer

    def get_queryset(self):
        tutorialName_id = self.kwargs['pk']
        
        post = TutorialPost.objects.filter(tutorialName_id=tutorialName_id)
        return post

#List of Post view
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TutorialPost.objects.all()
    serializer_class = TutorialPostSerializer   


class TutorialCommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        data = request.data.copy()
        data['user'] = request.user.id
        data['post'] = post_id
        data['username'] = request.user.username  # Add username to the data
        serializer = TutorialCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Print errors to console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_post_comments(request, post_id):
    try: 
        post_comments = Comment_tutorials.objects.filter(post_id=post_id)
        serializer = CommentGetTutSerializer(post_comments, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comments not found for this blog.'}, status=404)   



#Blog Post and delete view
class BlogPostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  # Assign the logged-in user to the post
        print(data)
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

#Blog Post and delete view
class MemePostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  # Assign the logged-in user to the post
        print(data)
        serializer = MemeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     
        

#Loggedin user Blogs
class BlogsUserListView(generics.ListCreateAPIView):
    queryset = Blogs.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        blog = Blogs.objects.filter(user=user)
        return blog

#Single blog view of user
class BlogsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogViewSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        blog_id = self.kwargs['blog_id']

        user = User.objects.get(id=user_id)
        blog = Blogs.objects.get(id=blog_id, user=user)

        return blog    
    
def get_blog_comments(request, blog_id):
    try:
        blog_comments = Comment.objects.filter(blog_id=blog_id)
        serializer = CommentGetSerializer(blog_comments, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comments not found for this blog.'}, status=404)    


@api_view(['POST'])
def create_contact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, blog_id):
        data = request.data.copy()
        data['user'] = request.user.id
        data['blog'] = blog_id
        data['username'] = request.user.username  # Add username to the data
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Print errors to console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def search_blog(request):
    query = request.GET.get('query', '')
    results = Blogs.objects.filter(title__icontains=query)
    data = [{'title': result.title, 'content': result.content, 'id':result.id, 'views':result.views,'date':result.date,'user':result.user} for result in results]
    return JsonResponse(data, safe=False)

def search_code(request):
    query = request.GET.get('query', '')
    results = CodeSnippet.objects.filter(title__icontains=query)
    data = [{'title': result.title, 'content': result.content, 'id':result.id, 'code':result.code} for result in results]
    return JsonResponse(data, safe=False)



#problem Post and delete view
class ProblemPostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  # Assign the logged-in user to the post
        print(data)
        serializer = ProblemSolveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
def contact_handler(request):
    if request.method == "POST":
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Send email to user
            subject = 'THANK YOU FOR CONTACTING ME'
            html_content = render_to_string('contact_email.html', {'name': serializer.data["name"]})
            text_content = strip_tags(html_content)  # Strip the html tag
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [serializer.data["email"]]
            msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # Send email notification to owner
            subject1 = 'HELLO SIR, YOU GOT A NEW MAIL'
            message1 = f'Hi k satyanarayana chary, Someone contacted you details are:- \nUsername: {serializer.data["name"]},\nEmail: {serializer.data["email"]},\nSubject: {serializer.data["subject"]},\nMessage: {serializer.data["message"]} \n'
            email_from = settings.EMAIL_HOST_USER
            recipient_list1 = ['acadamicfolio@gmail.com']
            send_mail(subject1, message1, email_from, recipient_list1)

            return Response({'message': 'Thanks for contacting me. I will look forward to utilizing this opportunity.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
