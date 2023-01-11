from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', views.UnFollowView.as_view(), name='unfollow'),
    path('profile_edit/<int:user_id>/', views.UserInfoEditView.as_view(), name='profile_edit'),

]
