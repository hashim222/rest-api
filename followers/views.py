from rest_framework import generics, permissions
from rest_api.permission import isOwnerOrReadOnly
from .serializers import FollowerSerializer
from .models import Follower


class FollowerList(generics.ListCreateAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [isOwnerOrReadOnly]
    queryset = Follower.objects.all()