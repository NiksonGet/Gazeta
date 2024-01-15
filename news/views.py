from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Post, Comment
import logging
from django.http import HttpResponse

from rest_framework import generics,viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import PostSerializer, CategorySerializer, CommentSerializer
from django.db.models import Q
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostListView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['time_added', 'category__id']

    start_date = datetime(2024, 1, 1)
    queryset = Post.objects.filter(Q(time_added__gte=start_date))

    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()

    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def user_comments(self, request):
        user_email = request.user.email

        try:
            # Получаем все комментарии от текущего пользователя
            user_comments = Comment.objects.filter(email=user_email)
            serializer = self.get_serializer(user_comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Comment.DoesNotExist:
            return Response({'error': 'No comments found for the user'}, status=status.HTTP_404_NOT_FOUND)


def print_post_history():
    all_posts = Post.objects.all()

    for post in all_posts:
        history_entries = post.history.all()

        print(f"History for post {post.title} (ID: {post.id}):")
        for entry in history_entries:
            print(f"  Version {entry.history_id} (changed at {entry.history_date}):")
            
            # Используем prev_record для получения предыдущей версии объекта
            prev_record = entry.prev_record
            if prev_record:
                print(f"    Previous version changed at {prev_record.history_date}")
            else:
                print("    Initial version")

            print("\n")
print_post_history()

db_logger = logging.getLogger('db')

def home(request):
    post = Post.objects.first()
    posts = Post.objects.all()[0:3]
    categories = Category.objects.all()[0:3]

    return render(request, 'home.html', {
        "post": post,
        "posts": posts,
        "categories": categories
    })


def posts(request):
    news = Post.objects.all()


    return render(request, 'news.html', {
        "news": news
    })


def categories(request):
    categories = Category.objects.all()

    return render(request, 'category.html', {
        'categories': categories
    })


def category(request, id):
    category = Category.objects.get(id=id)
    news = Post.objects.filter(category=category)

    return render(request, 'news-by-category.html', {
        "news": news,
        "category": category
    })


def post_details(request, id):
    post = Post.objects.get(pk=id)
    if request.method == 'POST':
        name = request.POST['name']
        comment = request.POST['message']
        email = request.POST['email']
        Comment.objects.create(
            post=post,
            title=name,
            email=email,
            content=comment
        )
        messages.success(request, 'Your comment now in moderation mode.')
    category = Category.objects.get(id=post.category.id)
    comments = Comment.objects.filter(post=post, status=True).order_by('-id')
    related_news = Post.objects.filter(category=category).exclude(id=id)


    return render(request, 'detail.html', {
        'news': post,
        'comments': comments,
        'related_news': related_news
    })
