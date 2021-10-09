"""api URL Configuration
"""

from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

app_name = "api"

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', views.UserSignUpViewSet.as_view({'get': 'list'})),
    path('signup/', views.UserSignUpViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('login/', views.UserLoginView.as_view(),  name="login"),
    path('addCategory/', views.AddCategoryView.as_view({'get': 'list', 'post': 'create'}),  name="category"),
    # path('retrieve/<int:pk>/', views.UserSignUpViewSet.as_view({'get': 'retrieve'})),
    # path('update/<int:pk>/', views.UserSignUpViewSet.as_view({'put': 'update'})),
    # path('remove/<int:pk>/', views.UserSignUpViewSet.as_view({'delete': 'destroy'})),

]


urlpatterns = format_suffix_patterns(urlpatterns)
