from django.urls import path
from .views import UsersView, Signup, Logout, MessagesView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', Logout.as_view()),
    path('signup/', Signup.as_view()),
    path('users/', UsersView.as_view()),
    path('messages/', MessagesView.as_view()),
]
