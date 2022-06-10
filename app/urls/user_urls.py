from django.urls import path
from app.views import user_views as views

urlpatterns = [

    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.registerUser, name="register"),
    path('all/', views.GetUsers.as_view(), name='all-users'),
    path('all/<str:pk>/', views.adminGetUser, name="admin_single_user"),
    path('admin/<str:pk>/', views.GetUserDetails.as_view(), name="admin"),
    path('<str:pk>/', views.UserProfile.as_view(), name="user-profile"),
    path('<str:pk>/update', views.updateUserProfile, name='update-user'),

]
