from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sign-in/', views.AccountSignInApi.as_view(), name='sign-in'),
    path('sign-up/', views.AccountSignUpApi.as_view(), name='sign-up'),
    path('profile/', views.ProfileApi.as_view(), name='profile'),
    path('logout/', views.AccountLogout.as_view(), name='logout'),
    path('members/', views.MembersApi.as_view(), name='members'),
    # path('changePassword/', views.ChangePassword.as_view(), name='changePassword'),
    path('update-member/', views.UpdateMemberApi.as_view(), name='update-member'),
    path('activate-member/', views.ActivateMemberApi.as_view(),  name='activate-member'),
    path('delete-member/', views.DeleteMemberApi.as_view(), name='delete-member'),
        path('change-password/', views.ChangePassword.as_view(), name='change-password'),
    # path('forgot-password/', views.ForgotPasswordApi.as_view(), name='forgot-password'),

]
#add media file root and url
