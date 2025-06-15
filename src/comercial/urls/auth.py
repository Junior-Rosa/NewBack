from django.urls import path
from .. import auth_views

urlpatterns = [
    path('login/', auth_views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.CustomLogoutView.as_view(), name='logout'),
    path('register/', auth_views.RegisterView.as_view(), name='register'),
    path('profile/', auth_views.ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', auth_views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('password-change/', auth_views.CustomPasswordChangeView.as_view(), name='password_change'),
]
