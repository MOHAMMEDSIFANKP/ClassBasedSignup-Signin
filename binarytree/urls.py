from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='Home'),
    path('form', SubmitForm.as_view(), name='SubmitForm'),
    path('signup/', Signup.as_view(), name='Signup'),
    path('signin/', Signin.as_view(), name='Signin'),
    path('signout/', signout.as_view(), name='signout'),
    
]
