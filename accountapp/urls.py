from django.urls import path

from accountapp.views import hello_world

app_name = 'accountapp' # 라우팅 편리하게 하기 위해서 작성해둔 것
urlpatterns = [
    path('hello_world/', hello_world, name='hello_world')
]