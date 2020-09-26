from rest_framework import serializers

from product.models import Category, Item, ItemImage

class imageSerializer(serializers.ModelSerializer):
    item = serializers.IntegerField(required=False)
    class Meta:
        fields = '__all__'
        model = ItemImage

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
    image = imageSerializer(many=True)

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
            'image',
        )
        model = Item
        depth = 0
        read_only_field = ("image")

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

    def create(self, validate_date,**kwagrs):
        image = validate_date.pop('image')
        item = Item.objects.create(**validate_date)
        print(len(image))
        for img in image:
            ItemImage.objects.create(img, item=item)
        return item

    def get_message(self, obj):
        return "Item added successfully"


