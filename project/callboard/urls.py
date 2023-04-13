from django.urls import path

from .views import PostList, PostDetail, ProfileView, PostCreate, PostDelete, PostUpdate, CommentDelete, AcceptResponse

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('create', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/delete_comment', CommentDelete.as_view(), name='comment_delete'),
    path('<int:pk>/accept_comment', AcceptResponse.as_view(), name='accept_comment'),



]

