from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.LoginViewPage.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('password/reset/', views.PasswordReset.as_view(), name='pass-reset'),
    path('password/reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='pass-reset-confirm'),
    path('password/reset/done/', views.PasswordResetDone.as_view(), name='pass-reset-done'),
    path('password/reset/complete/', views.PasswordResetComplete.as_view(), name='pass-reset-complete'),

    path('profile/', views.profile_view, name="profile"),
    path('<username>/', views.profile_view, name='userprofile'),
    path('profile/edit/', views.profile_edit, name="profile-edit"),
    path('profile/onboarding/', views.profile_edit, name="profile-onboarding"),
]
