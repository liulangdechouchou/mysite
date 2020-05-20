from django.urls import path,include
# from .views import blog_list
from . import views

#start with blog
urlpatterns = [
    # http://localhost:8000/blog/1
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_with_type>', views.blog_with_type, name='blog_with_type'),
    path('date/<int:year>/<int:month>', views.blog_with_date, name='blog_with_date'),
]