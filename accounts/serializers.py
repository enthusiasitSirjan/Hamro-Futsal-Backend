from rest_framework import serializers

from accounts.models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'password2', 'phone_number', 'address', 'user_role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            phone_number=self.validated_data['phone_number'],
            address=self.validated_data['address'],
            user_role=self.validated_data['user_role'],

        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        # fields = "__all__"
        exclude = ['is_admin', 'is_active', 'is_superuser', ]
        read_only_fields = ['id', 'is_admin', 'is_active', 'is_superuser', 'user_role']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
