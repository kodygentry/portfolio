from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='hunny-landing'),
    path('landing/', views.landing, name='hunny-landing'),
    path('signup/', views.signup, name='hunny-signup'),
    path('terms_service/', views.terms_service, name='hunny-terms_service'),
    path('login/', views.accountlogin, name='hunny-login'),
    path('profile/', views.profile, name='hunny-profile'),    
    path('profile-edit/', views.editProfile, name='hunny-edit-profile'),
    path('matchingroom/', views.matchingroom, name='hunny-matchingroom'),
    path('like_next/', views.like_next, name='hunny-like'),
    path('dislike_next/', views.dislike_next, name='hunny-dislike'),
    path('user/', views.user, name='hunny-user'),
    path('about/', views.about, name='hunny-about'),
    path('contact/', views.contact, name='hunny-contact'),
    path('logout/', views.accountlogout, name='hunny-logout'),
    path('settings/', views.settings, name='hunny-settings'),
    path('chat/', views.chat, name='hunny-chat'),
    path('chat/<str:room_name>/', views.chat_room, name='hunny-chat-room'),
    path('preferences/', views.preferences, name='hunny-preferences'),
    path('edit-preferences/', views.editPreferences, name='hunny-edit-preferences'),
    # path('settings/', views.settings, name='hunny-settings'),
    
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='settings.html'), 
        name='password_change'),

    # path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),
    #  name='password_reset_done'),

    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
    #  name='password_reset_complete'),
]
