from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import get_user_model, authenticate, login
from rest_framework.authentication import TokenAuthentication
from api.serializers import UserSignUpSerializer, UserLoginSerializer, NewCategorySerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import generics
from .models import Category

User = get_user_model()


class UserSignUpViewSet(viewsets.ModelViewSet):
    """
     A views for user signup.
    """
    serializer_class = UserSignUpSerializer
    queryset = User.objects.all()


class UserLoginView(generics.GenericAPIView):
    """
    A views for user login.
    """
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):

        data = request.data
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"message": f'User credentials are not correct.'},
                            status=HTTP_400_BAD_REQUEST)
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"message": f'Hello {user} you have Logged in Successfully', 'token': token.key},
                        status=HTTP_200_OK)


class AddCategoryView(viewsets.ModelViewSet):
    """
     A views for Add Category.
    """
    serializer_class = NewCategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """
        This view should return a list of all the categories of current user
        """
        return self.request.user.user_categories.all()


