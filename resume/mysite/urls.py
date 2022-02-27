from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('resume/', PublishedResume.as_view(), name='published_resume'),
    path('resume/post/<int:pk>/', ShowPost.as_view(), name='read_more'),
    path('resume/my_resume/', ShowUserPosts.as_view(), name='user_posts'),
    path('resume/language/<slug:lang_slug>/', PublishedByLanguages.as_view(), name='published_resume_by_languages'),
    path('add_resume/', AddResume.as_view(), name='add_resume'),
    path('update_resume/<int:pk>/', UpdateResume.as_view(), name='update-resume'),
    path('delete_resume/<int:pk>/', delete_resume, name='delete-resume'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]
