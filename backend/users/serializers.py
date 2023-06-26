from rest_framework import serializers

from .models import Follow, User


def subscribed(self, obj):
    user = self.context.get('request').user
    if user.is_anonymous:
        return False
    return Follow.objects.filter(user=user, author=obj.id).exists()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""
    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'email',
                  'password', 'is_subscribed']
        read_only_fields = ['id', 'is_subscribed']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

    def get_is_subscribed(self, obj):
        return subscribed(self, obj)


class PasswordChangeSerializer(serializers.Serializer):
    """Сериализатор смены пароля."""
    current_password = serializers.CharField(required=True,)
    new_password = serializers.CharField(required=True,)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Не верный пароль.')
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                'Новый пароль должен содержать не мене 8-ми символов.')
        return value


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор получения подписок."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed',)

    def get_is_subscribed(self, obj):
        return subscribed(self, obj)
