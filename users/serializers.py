from rest_framework import serializers

from users.models import Users


class UsersRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'first_name', 'last_name', 'email', 'last_login', 'password')
        read_only_fields = ('id', 'last_login')

    def create(self, validated_data):
        password = validated_data.get("password")
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
