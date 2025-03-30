from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404  # Ensure correct import
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from notifications.models import Notification  # Import Notification model

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        # Create a notification when a new post is created
        Notification.objects.create(
            recipient=self.request.user,
            actor=self.request.user,
            verb="posted",
            target=post
        )

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
        """Retrieve posts from followed users."""
        user = request.user
        following_users = user.following.all()  # Ensure following_users is defined
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # Create a notification when a comment is added
        Notification.objects.create(
            recipient=comment.post.author,
            actor=self.request.user,
            verb="commented on",
            target=comment.post
        )

class FeedView(generics.ListAPIView):
    """Retrieve posts from followed users."""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()  # Ensure following_users is defined
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Like a post."""
        post = generics.get_object_or_404(Post, pk=pk)  # Ensuring correct usage of generics.get_object_or_404
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({"message": "Already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a notification when a post is liked
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked",
            target=post
        )

        return Response({"message": "Post liked successfully"}, status=status.HTTP_201_CREATED)

class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Unlike a post."""
        post = generics.get_object_or_404(Post, pk=pk)  # Correct usage of generics.get_object_or_404
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"message": "Post unliked successfully"}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"message": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)
