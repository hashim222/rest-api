from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from rest_api.permission import isOwnerOrReadOnly


class PostList(APIView):
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get(self, request):
        posts = Post.objects.all()

        serializer = PostSerializer(
            posts, many=True,
            context={'request': request}
        )
        # print('[ This is Post Serializer Data: ', serializer.data,  ']')

        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        print('[ This is Post serializer: ', serializer,  ']')

        if serializer.is_valid():
            serializer.save(owner=request.user)
            print('[ This is save user data: ',
                  serializer.save(owner=request.user),  ']')

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    serializer_class = PostSerializer
    permission_classes = [
        isOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            posts = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, posts)
            return posts
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        posts = self.get_object(pk)
        serializer = PostSerializer(posts, context={
            'request': request
        })
        return Response(serializer.data)

    def post(self, request, pk):
        posts = self.get_object(pk)
        serializer = PostSerializer(posts, data=request.data, context={
            'request': request
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        posts = self.get_object(pk)
        posts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
