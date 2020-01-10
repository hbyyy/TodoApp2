from django.urls import path

from members.views import signup_view

app_name = 'members'

urlpatterns = [
    path('signup/', signup_view, name='signup')
]