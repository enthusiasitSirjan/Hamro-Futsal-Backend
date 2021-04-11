from django.urls import path

from accounts.views import *

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('edit_user/<pk>', EditUserDetails.as_view()),
    path('change_password/', ChangePassword.as_view()),
    path('verify_email/', EmailVerify.as_view()),
    path('all_users/', ListAllUserAccounts.as_view()),
    path('all_futsal_owners/', ListAllFutsalOwnerAccounts.as_view()),
    path('forgot_password/', CreatePin.as_view()),
    path('forgot_password/change/',ChangePasswordWithPin.as_view()),
    path('deleteUser/<pk>',UserAccountDelete.as_view()),
    path('deleteOwner/<pk>',FutsalOwnerDelete.as_view())
]
