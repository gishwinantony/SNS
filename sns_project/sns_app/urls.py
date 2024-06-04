from django.urls import path
from .views import CreateUserAPIView,AuthenticateUserAPIView,SendRequestAPIView,AcceptRequestAPIView,PendingRequestsAPIView,FriendsAPIView,UserSearchAPIView



urlpatterns = [
    path ('signup',CreateUserAPIView.as_view ()),
    path('login',AuthenticateUserAPIView.as_view()),
    path ('send',SendRequestAPIView.as_view ()),
    path ('<int:id>/accept',AcceptRequestAPIView.as_view ()),
    path ('pending',PendingRequestsAPIView.as_view ()),
    path('friends',FriendsAPIView.as_view()),
    path('search',UserSearchAPIView.as_view())


    
]