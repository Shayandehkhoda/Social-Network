from django.urls import path
from . import views
from .feeds import LatestEntriesFeed

app_name = 'social'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('page/<int:pnum>/', views.HomeView.as_view(), name='home'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/update/<slug:slug>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<slug:slug>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='detail'),
    path('comment_reply/<slug:post_slug>/<int:comment_id>/', views.CommentReplyView.as_view(), name='cmreply'),
    path('like/<slug:post_slug>/', views.LikePostView.as_view(), name='like_post'),
    path('search', views.SearchView.as_view(), name='search'),
    path('followingfeed/', views.FollowingFeedView.as_view(), name='followingfeed'),
    path('latestfeed/', LatestEntriesFeed(), name='rssfeed'),
]
