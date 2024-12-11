from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from .models import Server
from .serializer import ServerSerializer

class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()
    
    def list(self, request):
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        # Start with the base queryset
        queryset = self.queryset

        # if by_user and not request.user.is_authenticated:
        #     raise AuthenticationFailed()
        if by_user or by_serverid and not request.user.is_authenticated:
            raise AuthenticationFailed()

        if category:
            queryset = queryset.filter(category=category)

        if by_user:
            user_id = request.user.id
            queryset = queryset.filter(member=user_id)

        if qty:
            queryset = queryset[: int(qty)]

        if by_serverid:
            try:
                server_id = int(by_serverid)
                queryset = queryset.filter(id=server_id)  # Filter by server ID
                if not queryset.exists():
                    raise ValidationError(detail=[f"Server with ID {server_id} not found"])
            except ValueError:
                raise ValidationError(detail=[f"Server value error"])


        serializer = ServerSerializer(queryset, many=True)
        return Response(serializer.data)