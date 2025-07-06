from django.urls import path
from .views import list_blogs, blog_detail, create_blog, update_blog, delete_blog

urlpatterns = [
    path('', list_blogs, name='list_blogs'),
    path('<int:blog_id>/', blog_detail, name='blog_detail'),
    path('create/', create_blog, name='create_blog'),
    path('<int:blog_id>/update/', update_blog, name='update_blog'),
    path('<int:blog_id>/delete/', delete_blog, name='delete_blog'),
]
