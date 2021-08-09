from django.urls import path

from commentapp.views import CommentCreateView

urlpatterns = [
    path('create/', CommentCreateView.as_view(), name='create'),
]