from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author_name = models.CharField(max_length=255)
    author_image = models.ImageField(upload_to='blog_authors/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class BlogAttachment(models.Model):
    blog = models.ForeignKey(BlogPost, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='blog_attachments/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.blog.title}"
