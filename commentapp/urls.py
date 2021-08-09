from django.urls import path

from commentapp.views import CommentCreateView, CommentDeleteView

urlpatterns = [
    path('create/', CommentCreateView.as_view(), name='create'),
    path('delete<int:pk>', CommentDeleteView.as_view())
]