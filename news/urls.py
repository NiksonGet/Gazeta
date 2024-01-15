from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import PostListView, CategoryListView, CommentViewSet

urlpatterns = [
    path('', views.home, name='home'),
    path('news', views.posts, name='news'),
    path('category/<int:id>', views.category, name='category'),
    path('categories', views.categories, name='categories'),
    path('detail/<int:id>', views.post_details, name='details'),
    path('api/posts/', PostListView.as_view(), name='post-list'),
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/comments/user_comments/', CommentViewSet.as_view({'get': 'user_comments'}), name='user-comments'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
