from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from products.serializers import ProductSerializer
from products.models import Product

from rest_framework.views import APIView
from rest_framework import authentication, permissions
# Create your views here.
class ProductView(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        data = Product.objects.all()
        serializer = ProductSerializer(data, many=True)
        return JsonResponse(serializer.data, status=201, safe=False)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
class SingleProductView(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)
    
    def get(self, request, pk, format=None):
        try:
            product = Product.objects.get(id=pk)
        except (Product.DoesNotExist):
            data = {"message": "Product doesn't exist"}
            return JsonResponse(data, status=400)
        serializer = ProductSerializer(product, many=False)
        return JsonResponse(serializer.data, status=201, safe=False)

    def put(self, request, pk):
        data = JSONParser().parse(request)
        try:
            product = Product.objects.get(id=pk)
        except (Product.DoesNotExist):
            data = {"message": "Product doesn't exist"}
            return JsonResponse(data, status=400)
        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except (Product.DoesNotExist):
            data = {"message": "Product doesn't exist"}
            return JsonResponse(data, status=400)
        product.delete()
        return JsonResponse({"message": "Product with id `{}` has been deleted.".format(pk)}, status=204)