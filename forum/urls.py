from django.urls import path
from .views import *



urlpatterns = [
    path('', home, name = "home"),
    path('create-post/', create_post , name = 'create-post'),
    path('edit-post/<pk>', edit_post, name= 'edit-post'),
    path('delete-post/<pk>', delete_post, name = 'delete-post'),
    path('logout/', logout_user, name ='logout' ),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('post/<pk>', post_page , name = 'post-page'),
    path('delete-comment/<pk>', delete_comment , name='delete-comment'),
    path('edit-comment/<post>/<pk>', edit_comment , name='edit-comment')
]
