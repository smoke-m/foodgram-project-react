from djoser.serializers import UserCreateSerializer

from api.serializers import MiniRecipeSerializer, serializers
from .models import User


class CreteUserSerializer(UserCreateSerializer):
    """Сериализатор регистрации модели User."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'email',
                  'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserSerializer(UserCreateSerializer):
    """Сериализатор модели User."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'email',
                  'is_subscribed']
        read_only_fields = ['id', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.follow.exists()


class FollowSerializer(UserSerializer):
    """Сериализатор получения подписок."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count']
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return MiniRecipeSerializer(recipes, many=True).data

    def validate(self, attrs):
        if self.context['request'].user == self.instance:
            raise serializers.ValidationError('Нельзя подписаться на себя!')
        return attrs
