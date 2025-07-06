from django.contrib import admin
from .models import BlogPost, BlogAttachment


class BlogAttachmentInline(admin.TabularInline):
    model = BlogAttachment
    extra = 0


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'created_at')
    inlines = [BlogAttachmentInline]
