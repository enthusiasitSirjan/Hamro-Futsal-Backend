import random

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, status, request
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, ListAPIView, \
    RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.Email import Test, SendVerifyToken
from accounts.models import Account, VerificationTokens, ForgotPasswordPin
from accounts.permission import IsMine
from accounts.serializers import RegistrationSerializer, UserEditSerializer, ChangePasswordSerializer, \
    ForgotPasswordSerializer


# @api_view(['POST', ])
# @permission_classes([])
# @authentication_classes([])
# def registration_view(request):
class RegistrationView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        if request.method == 'POST':
            data = {}
            email = request.data.get('email', '0').lower()
            if validate_email(email) != None:
                data['error_message'] = 'That email is already in use.'
                data['response'] = 'Error'
                return Response(data, status=400)

            username = request.data.get('username', '0')
            if validate_username(username) != None:
                data['error_message'] = 'That username is already in use.'
                data['response'] = 'Error'
                return Response(data, status=400)

            serializer = RegistrationSerializer(data=request.data)

            if serializer.is_valid():
                account = serializer.save()
                data['response'] = 'Successfully registered new user.'
                return Response(data, status=200)

            else:
                data = serializer.errors
                return Response(data, status=400)


class EditUserDetails(RetrieveUpdateAPIView):
    def get_queryset(self):
        return Account.objects.filter(email=self.request.user)

    serializer_class = UserEditSerializer
    permission_classes = []


class ListAllUserAccounts(ListAPIView):
    def get_queryset(self):
        return Account.objects.filter(user_role='USER')

    serializer_class = UserEditSerializer
    permission_classes = []


class UserAccountDelete(RetrieveDestroyAPIView):
    def get_queryset(self):
        return Account.objects.filter(user_role='USER')

    serializer_class = UserEditSerializer
    permission_classes = []


class ListAllFutsalOwnerAccounts(ListAPIView):
    def get_queryset(self):
        return Account.objects.filter(user_role='OWNER')

    serializer_class = UserEditSerializer
    permission_classes = []


class FutsalOwnerDelete(RetrieveDestroyAPIView):
    def get_queryset(self):
        return Account.objects.filter(user_role='OWNER')

    serializer_class = UserEditSerializer
    permission_classes = []


def validate_email(email):
    account = None
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return None
    if account != None:
        return email


def validate_username(username):
    account = None
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return None
    if account != None:
        return username


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = {}
        email = request.POST.get('email')
        password = request.POST.get('password')
        account = authenticate(email=email, password=password)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            data['response'] = 'Successfully authenticated.'
            data['pk'] = account.pk
            data['email'] = email.lower()
            data['token'] = token.key
            data['user_role'] = account.user_role
            data['username'] = account.username

            return Response(data, status=200)
        else:
            data['response'] = 'Error'
            data['error_message'] = 'Invalid credentials'

            return Response(data, status=400)


class ChangePassword(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Account

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=400)

            # confirm the new passwords match
            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")
            if new_password != confirm_new_password:
                return Response({"new_password": ["New passwords must match"]}, status=400)
            # Check new pass same as old
            a = self.request.user
            if a.check_password(serializer.data.get("new_password")):
                return Response({"error_message": "New Password can't be same as old."},
                                status=400)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"response": "Successfully changed password"}, status=200)

        return Response(serializer.errors, status=400)


class EmailVerify(APIView):
    def post(self, request):
        token = request.data["token"]
        if VerificationTokens.objects.filter(token=token):
            user = VerificationTokens.objects.filter(token=token).values()
            user_id = user[0]["user_id"]
            Account.objects.filter(id=user_id).update(is_active=True)
            VerificationTokens.objects.filter(token=token).delete()

            print(user)
            return Response({"message": "Email verified successfully"})
        return Response({"error_msg": "Token Not found"})

    permission_classes = []
    authentication_classes = []


class CreatePin(APIView):
    def post(self, request):
        user_email = request.data['email']
        if Account.objects.filter(email=user_email):
            pin = str(random.randint(200000, 600000))
            user = Account.objects.filter(email=user_email)[0]
            ForgotPasswordPin.objects.create(forgot_pin=pin, user=user)
            SendVerifyToken(pin, user_email)
            return Response({"message": "PIN is sent to your email"})
        return Response({"error_msg": "Email Not found"})

    permission_classes = []
    authentication_classes = []


class ChangePasswordWithPin(APIView):
    def post(self, request):
        pin = request.data['pin']
        new_password = request.data['new_password']
        if ForgotPasswordPin.objects.filter(forgot_pin=pin):
            user = ForgotPasswordPin.objects.filter(forgot_pin=pin).values()
            user_id = user[0]['user_id']
            print("User:", user_id)
            account = Account.objects.filter(id=user_id)[0]
            account.set_password(new_password)
            account.save()
            return Response({"message": "Password Changed successfully"})
        return Response({"error_msg": "Token Not found"})

    permission_classes = []
    authentication_classes = []
