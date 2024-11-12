from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView

# Create your views here.
class Operations(APIView):
    def post(self,request):
        serializer=ItemSerializer(data=request.data)
        if(serializer.is_valid()):
            email=serializer.validated_data['email']
            if(Items.objects.filter(email=email).exists()):
                return Response({"message: Already Exists"},status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            item=Items.objects.get(pk=pk)
        except Items.DoesNotExist:
            return Response({"message: Something went wrong"},status=status.HTTP_400_BAD_REQUEST)
        
        item.delete()
        return Response({"message: Data Deleted"},status=status.HTTP_204_NO_CONTENT)
    
    def get(self,request):
        item=Items.objects.all()
        serializer=ItemSerializer(item,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,email):
        try:
            item=Items.objects.get(email=email)
        except Items.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer=ItemSerializer(item,data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class Book(APIView):

    def put(self,request,pk):
        try:
            item=Items.objects.get(pk=pk)
        except Items.DoesNotExist:
            return Response({"message : Something Went Wrong"},status=status.HTTP_400_BAD_REQUEST)
        if('books_borrowed' in request.data):
            new_books_borrowed=request.data['books_borrowed']
            if(new_books_borrowed>=item.max_books):
                return Response({"message: Limit Exceded"},status=status.HTTP_400_BAD_REQUEST)
            item.books_borrowed=new_books_borrowed
            item.save()
            return Response({"message: Books Borrowed Sucessfully"},status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class Over(APIView):
    def get(self,request):
        item=Items.objects.filter(overdue_fees__gte=10)
        serializer=ItemSerializer(item,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
