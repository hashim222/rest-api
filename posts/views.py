from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer


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
        print('[ This is Post Serializer Data: ', serializer.data,  ']')

        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        print('[ This is Post serializer: ', serializer,  ']')

        if serializer.is_valid():
            serializer.save(owner=request.user)
            print('[ This is save user data: ', serializer.save(owner=request.user),  ']')

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
