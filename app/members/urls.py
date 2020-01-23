from django.urls import path

from members.views import signup_view, logout_view, naver_signup_view, facebook_signup_view

app_name = 'members'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('naver-signup', naver_signup_view, name='naver_signup'),
    path('facebook-signup', facebook_signup_view, name='facebook_signup'),

]
