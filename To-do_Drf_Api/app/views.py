"""
Views for app.
"""
from app.models import *
from app.serializers import *

from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication


def hello_drf(self):
    """
    Get the requested url, return json response.
    """
    return HttpResponse("Hello, Django REST Framework!!")


# api_view
@api_view(['GET','POST','PUT','PATCH','DELETE',])
def hello_world(request):
    """
    Returns messages by given request.
    """
    if request.method == 'GET':
        return Response({"Message": "Hello, World!"})

    elif request.method == 'POST':
        return Response({"Message": "Hello, You hit POST request!"})
    
    elif request.method == 'PUT':
        return Response({"Message": "Hello, You hit PUT request!"})

    elif request.method == 'PATCH':
        return Response({"Message": "Hello, You hit PATCH request!"})

    elif request.method == 'DELETE':
        return Response({"Message": "Hello, You hit DELETE request!"})


# APIView
class HelloJWTView(APIView):
    """
    TEST jwt authentication.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        content = {
            "MSG": f"Hello {user}, JWT Authentication is work".title(),
        }
        return Response(content)


class TagsView(APIView):
    """
    Handle list and create tasks for authenticated users.
    """
    serializer = TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request, *args, **kwargs):

        tag_obj = Tag.objects.filter(user=request.user)
        serializer = self.serializer(tag_obj,many=True)

        if serializer.data == []:

            return Response({"INFO": "No Tag Available"})

        return Response({"Tags": serializer.data})

    def post(self,request, *args, **kwargs):

        serializer = self.serializer(data=request.data)
        
        if serializer.is_valid():

            serializer.save(user=request.user)
        
            return Response({
                "Message":"Tag Created successfully!!",
                "Url": "http://127.0.0.1:8000/api/app/tags/"
            })
        
        return Response({
            "error": serializer.errors
        })


class TagsDetailsView(APIView):
    """
    Handle retrieving, updating and deleting tasks of authenticated user by id's.
    """
    serializer = TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,tags_id: int):

        try:
            tags_obj = Tag.objects.get(user=request.user,id=tags_id)
            serializer = self.serializer(tags_obj)

            return Response({
                "Tags": serializer.data
            })
        except Tag.DoesNotExist:

            return Response({
                "Info": "Tags not found",
                "Message": "Please enter valid tag id."
            })

    def put(self,request,tags_id: int):

        try:
            tags_obj = Tag.objects.get(user=request.user,id=tags_id)
            serializer = self.serializer(tags_obj, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response({
                    "Message": "Tag Updated successfully!!",
                    "Tags": serializer.data
                })

            return Response({
                "Error": serializer.errors
            })

        except Tag.DoesNotExist:

            return Response({
                "Info": "Tag not found",
                "Message": "Please enter valid Tag id."
            })
        
    def patch(self,request,tags_id: int):

        try:

            tags_obj = Tag.objects.get(user=request.user, id=tags_id)
            serializer = self.serializer(tags_obj, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                
                return Response({
                    "Message": "Tag updated successfully!!",
                    "Tags": serializer.data
                })
            
            return Response({
                "Error": serializer.errors
            })

        except Tag.DoesNotExist:

            return Response({
                "Info": "Tag not found",
                "Message": "Please enter valid tag id."
            })
        
    def delete(self,request,tags_id: int):

        try:
            tags_obj = Tag.objects.get(user=request.user, id=tags_id)
            tags_obj.delete()

            return Response({
                "Message": "Tag deleted successfully!!",
                "Url": "http://127.0.0.1:8000/api/app/tags/"
            })
        
        except Tag.DoesNotExist:

            return Response({
                "Info": "Tag not found",
                "Message": "May tag already deleted or may not created."
            })


# Generic view
class TaskGenericView(generics.ListCreateAPIView):
    """
    Handle listing and creating todo objects.
    """
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve authenticated user.
        """
        queryset = self.queryset
        
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new task.
        """
        serializer.save(user=self.request.user)


class TaskDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handle retrieving, updating or deleting objects for authenticated users.
    """
    serializer_class = TodoDetailSerializer
    queryset = Todo.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve and return authenticated users.
        """
        queryset = self.queryset
        return queryset.filter(user=self.request.user)


# ViewSets
class HelloViewSet(viewsets.ViewSet):
    """
    TEST Api view.
    """
    serializer_class = HelloSerializer
    permission_classes = [IsAuthenticated]

    def list(self,request):
        """
        Return a message.
        """
        return Response({"MSG":"Hello, Django REST Framework"})

    def create(self,request):
        """
        Create a new message.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            msg = f'Hello, {first_name} {last_name}'

            return Response({
                'DATA': msg
            })

        else:

            return Response({
                "ERR": serializer.errors
            })


class CreateUserView(generics.CreateAPIView):
    """
    Handle creating a new user.
    """
    serializer_class = UserSerializer   


class CreateTokenView(ObtainAuthToken):
    """
    Handle create user authentication token.
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ChangePasswordView(generics.UpdateAPIView):
    """
    Handle an endpoint change password.
    """
    model = User
    serializer_class = ChangePasswordSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieve and return authenticated user.
        """
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        """
        Update password with hashes formate.
        """
        self.obj = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check password
            if not self.obj.check_password(serializer.data['old_password']):
                return Response({"Message": "Please enter current password!!"})
            
            # Set password with hashes formate
            new_password = serializer.data['new_password']
            conform_password = serializer.data['conform_password']

            if new_password == conform_password:

                self.obj.set_password(conform_password)
                self.obj.save()
                response = {
                    "Message": "Password Changed successfully",
                    "Data":[]
                }

                return Response(response)
            
            return Response({"ERROR": "Please enter same password"})
        
        return Response({"ERROR": serializer.errors})


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Handle retrieve and update authenticated user.
    """
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieve and return authenticated user.
        """
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class StudentViewSet(viewsets.ModelViewSet):
    """
    Retrieves, updates and deletes student.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # If we don't want to paginate the results.
    pagination_class = None