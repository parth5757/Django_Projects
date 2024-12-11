from django.shortcuts import render
from rest_framework import viewsets
from .serializer import ServerSerializer
from .models import Server
from rest_framework.response import Response

class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    # def list(self, request):

    #     category = request.query_params.get("category")
    #     qty = request.query_params.get("qty")
    #     by_user = request.query_params.get("by_user") == "true"

    #     # Start with the base queryset
    #     queryset = self.queryset

    #     if category:
    #         self.queryset.filter(category=category) 

    #     if by_user:
    #         user_id = request.user.id
    #         self.queryset = self.queryset.filter(member=user_id)

    #     if qty:
    #         self.queryset = self.queryset[: int[qty]]

    #     serializer = ServerSerializer(self.queryset, many=True)
    #     return Response(serializer.data)
    
    def list(self, request):
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"

        # Start with the base queryset
        queryset = self.queryset

        if category:
            queryset = queryset.filter(category=category)

        if by_user:
            user_id = request.user.id
            queryset = queryset.filter(member=user_id)

        if qty:
            queryset = queryset[: int(qty)]

        serializer = ServerSerializer(queryset, many=True)
        return Response(serializer.data)
