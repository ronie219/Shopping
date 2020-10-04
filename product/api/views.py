from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from django.shortcuts import get_object_or_404

from product.api.serializer import categorySerializer, itemSerializer
from product.models import Category, Item


class categoryCreations(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        obj = categorySerializer(data=request.data)
        obj.is_valid(raise_exception=True)
        obj.save()
        return Response(obj.data, status=201)

    def get(self, request, id=None):
        try:
            if id:
                item = Category.objects.get(id=id)
                obj = categorySerializer(item)
            else:
                item = Category.objects.all()
                obj = categorySerializer(item, many=True)
        except Category.DoesNotExist:
            return Response({"Error Message": "No Category Found"}, status=404)
        return Response(obj.data, status=200)

    def put(self, request, id=None):
        try:
            if id:
                instance = Category.objects.get(id=id)
                obj = categorySerializer(instance=instance, data=request.data)
                obj.is_valid(raise_exception=True)
                obj.save()
                return Response(obj.data, status=200)
            else:
                return Response({"Error Message": "Id is Must"}, status=404)
        except Category.DoesNotExist:
            return Response({"Error Message": "No Category Found"}, status=404)

    def delete(self, request, id=None):
        print(request)
        try:
            if id:
                Category.objects.get(id=id).delete()
                return Response({"Error Message": "Delete SuccessFully"}, status=200)
            else:
                return Response({"Error Message": "Id is Must"}, status=404)
        except Category.DoesNotExist:
            return Response({"Error Message": "No Category Found"}, status=404)


class itemCreations(ListAPIView,
                    CreateModelMixin, 
                    UpdateModelMixin, 
                    DestroyModelMixin):
    serializer_class = itemSerializer
    lookup_field = 'id',
    # queryset = Item.objects.all()

    def get_queryset(self):
        super_qs = Item.objects.all()
        qs = self.request.GET.get('q')
        if qs is not None:
            super_qs = Item.objects.filter(id=qs)
        return super_qs

    def get_object(self):
        passed_id = self.request.GET.get('id')
        query_set = self.get_queryset()
        obj = None
        if passed_id is not None:
            obj = get_object_or_404(query_set, id=passed_id)
            self.check_object_permissions(self.request, obj)
        return obj

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return self.create(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def patch(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)