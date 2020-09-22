from rest_framework import serializers

from product.models import Category, Item


class categorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def create(self, validate_date):
        return Category.objects.create(**validate_date)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    def validate(self, data):
        if data['name'] is None or "":
            raise serializers.ValidationError("mandototy be need")
        try:
            Category.objects.get(name=data['name'])
            raise serializers.ValidationError("Already exist")
        except Category.DoesNotExist:
            return data

    class Meta:
        fields = [
            'id',
            'category',
        ]


class itemSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'user',
            'id',
            'name',
            'category',
            'prize',
            'description',
            'count',
            'message',
        )
        model = Item
        depth = 0

    def validate(self, data):
        name = data.get('name')
        category = data.get('category')
        length = len(data['description'])
        if length < 3:
            raise serializers.ValidationError("Description Length must be greater than 3")
        a = Item.objects.filter(name__iexact=name, category__id__iexact=category.id)
        if a.exists():
            raise serializers.ValidationError("Product already exist")

        return data

    def create(self, validate_date):
        return Item.objects.create(**validate_date)

    def get_message(self, obj):
        return "Item added successfully"