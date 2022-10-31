from rest_framework import generics, permissions
from rest_api.permission import isOwnerOrReadOnly
from .models import Like
from .serializers import LikeSerializer


class LikeList(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [isOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
