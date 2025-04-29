from django.urls import path
from . import views
from .views import DetailPost
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('new/', views.post_create, name='post_create'),
    path('prof/', views.post_prof, name='post_prof'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'), 
    path('detail/<int:pk>', DetailPost.as_view(), name='detail'), 
    path('post/<int:post_id>/reply/', views.add_reply, name='add_reply'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
]
