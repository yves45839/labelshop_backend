import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from .models import BlogPost, BlogAttachment


def serialize_blog(blog, request=None):
    data = model_to_dict(blog, fields=['id', 'title', 'content', 'author_name', 'created_at', 'updated_at'])
    data['author_image'] = request.build_absolute_uri(blog.author_image.url) if blog.author_image else None
    data['attachments'] = [
        request.build_absolute_uri(att.file.url) if request else att.file.url
        for att in blog.attachments.all()
    ]
    return data


def list_blogs(request):
    blogs = BlogPost.objects.prefetch_related('attachments').all()
    result = [serialize_blog(blog, request) for blog in blogs]
    return JsonResponse(result, safe=False)


def blog_detail(request, blog_id):
    try:
        blog = BlogPost.objects.prefetch_related('attachments').get(id=blog_id)
    except BlogPost.DoesNotExist:
        return JsonResponse({'error': 'Blog not found'}, status=404)
    return JsonResponse(serialize_blog(blog, request))


@csrf_exempt
@login_required
def create_blog(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    title = request.POST.get('title')
    content = request.POST.get('content')
    author_name = request.POST.get('author_name')

    if not title or not content or not author_name:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    blog = BlogPost.objects.create(
        title=title,
        content=content,
        author_name=author_name,
        author_image=request.FILES.get('author_image'),
    )

    for file in request.FILES.getlist('attachments'):
        BlogAttachment.objects.create(blog=blog, file=file)

    return JsonResponse(serialize_blog(blog, request), status=201)


@csrf_exempt
@login_required
def update_blog(request, blog_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        blog = BlogPost.objects.get(id=blog_id)
    except BlogPost.DoesNotExist:
        return JsonResponse({'error': 'Blog not found'}, status=404)

    title = request.POST.get('title')
    content = request.POST.get('content')
    author_name = request.POST.get('author_name')

    if title:
        blog.title = title
    if content:
        blog.content = content
    if author_name:
        blog.author_name = author_name
    if 'author_image' in request.FILES:
        blog.author_image = request.FILES['author_image']
    blog.save()

    for file in request.FILES.getlist('attachments'):
        BlogAttachment.objects.create(blog=blog, file=file)

    return JsonResponse(serialize_blog(blog, request))


@csrf_exempt
@login_required
def delete_blog(request, blog_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        blog = BlogPost.objects.get(id=blog_id)
    except BlogPost.DoesNotExist:
        return JsonResponse({'error': 'Blog not found'}, status=404)
    blog.delete()
    return JsonResponse({'message': 'Blog deleted'})
