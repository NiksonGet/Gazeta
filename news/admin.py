from django.contrib import admin
from .models import Category, Post, Comment, Tag
from import_export.admin import ImportExportModelAdmin


class CategoryPostInline(admin.TabularInline):
    model = Post
    extra = 1


class AdminCategory(ImportExportModelAdmin,admin.ModelAdmin):
    inlines = [CategoryPostInline]
    list_display = ('title', 'date_created', 'date_updated')
    list_filter = ['date_created', 'date_updated']
    search_fields = ['title']
    date_hierarchy = 'date_created'


admin.site.register(Category, AdminCategory)


class AdminPost(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('title', 'category',  'time_added')
    list_display_links = ['title', 'category', 'time_added']
    list_filter = ['category', 'time_added', 'tags']
    search_fields = ['title']
    date_hierarchy = 'time_added'
    filter_horizontal = ['tags']



class AdminComment(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('title', 'post', 'email', 'content', 'status')
    list_filter = ['status', 'post']
    search_fields = ['post__title', 'title']
    raw_id_fields = ['post']


class AdminTag(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('title', 'date_created')
    list_filter = ['date_created']
    search_fields = ['title']
    raw_id_fields = ['post']


admin.site.register(Post, AdminPost)
admin.site.register(Comment, AdminComment)
admin.site.register(Tag, AdminTag)


