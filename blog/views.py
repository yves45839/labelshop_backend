import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BlogPost, BlogAttachment


def serialize_blog(blog, request=None):
    def build_url(field):
        try:
            if not field:
                return None
            url = field.url
            return request.build_absolute_uri(url) if request else url
        except Exception:
            return None

    try:
        attachments = [
            request.build_absolute_uri(att.file.url) if request else att.file.url
            for att in blog.attachments.all()
        ]
    except Exception:
        attachments = []

    return {
        'id': blog.pk,
        'title': blog.title,
        'content': blog.content,
        'author_name': blog.author_name,
        'author_image': build_url(blog.author_image),
        'published_date': blog.published_date.isoformat() if blog.published_date else None,
        'category': blog.category,
        'language': blog.language,
        'attachments': attachments,
        'created_at': blog.created_at.isoformat() if blog.created_at else None,
        'updated_at': blog.updated_at.isoformat() if blog.updated_at else None,
    }


def _cors(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


def list_blogs(request):
    if request.method == 'OPTIONS':
        return _cors(JsonResponse({}, status=200))
    blogs = BlogPost.objects.prefetch_related('attachments').all()
    return _cors(JsonResponse([serialize_blog(b, request) for b in blogs], safe=False))


def blog_detail(request, blog_id):
    if request.method == 'OPTIONS':
        return _cors(JsonResponse({}, status=200))
    try:
        blog = BlogPost.objects.prefetch_related('attachments').get(id=blog_id)
    except BlogPost.DoesNotExist:
        return _cors(JsonResponse({'error': 'Blog not found'}, status=404))
    return _cors(JsonResponse(serialize_blog(blog, request)))


@csrf_exempt
def create_blog(request):
    if request.method == 'OPTIONS':
        return _cors(JsonResponse({}, status=200))
    if request.method != 'POST':
        return _cors(JsonResponse({'error': 'Method not allowed'}, status=405))

    # Accepte JSON ou multipart form
    content_type = request.content_type or ''
    if 'application/json' in content_type:
        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, Exception):
            return _cors(JsonResponse({'error': 'JSON invalide'}, status=400))
        title        = body.get('title', '').strip()
        content      = body.get('content', '').strip()
        author_name  = body.get('author_name', '').strip()
        published_date = body.get('published_date') or None
        category     = body.get('category', '')
        language     = body.get('language', '')
        author_image = None
    else:
        title        = request.POST.get('title', '').strip()
        content      = request.POST.get('content', '').strip()
        author_name  = request.POST.get('author_name', '').strip()
        published_date = request.POST.get('published_date') or None
        category     = request.POST.get('category', '')
        language     = request.POST.get('language', '')
        author_image = request.FILES.get('author_image')

    if not title or not content or not author_name:
        return _cors(JsonResponse({'error': 'Missing required fields: title, content, author_name'}, status=400))

    blog = BlogPost.objects.create(
        title=title,
        content=content,
        author_name=author_name,
        author_image=author_image,
        published_date=published_date,
        category=category,
        language=language,
    )

    if not ('application/json' in content_type):
        for file in request.FILES.getlist('attachments'):
            BlogAttachment.objects.create(blog=blog, file=file)

    return _cors(JsonResponse(serialize_blog(blog, request), status=201))


@csrf_exempt
def update_blog(request, blog_id):
    if request.method == 'OPTIONS':
        return _cors(JsonResponse({}, status=200))
    if request.method not in ('POST', 'PATCH', 'PUT'):
        return _cors(JsonResponse({'error': 'Method not allowed'}, status=405))

    try:
        blog = BlogPost.objects.get(id=blog_id)
    except BlogPost.DoesNotExist:
        return _cors(JsonResponse({'error': 'Blog not found'}, status=404))

    content_type = request.content_type or ''
    if 'application/json' in content_type:
        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, Exception):
            return _cors(JsonResponse({'error': 'JSON invalide'}, status=400))
        for field in ('title', 'content', 'author_name', 'published_date', 'category', 'language'):
            if field in body:
                val = body[field]
                if field == 'published_date' and val == '':
                    val = None
                setattr(blog, field, val)
    else:
        for field in ('title', 'content', 'author_name', 'category', 'language'):
            val = request.POST.get(field)
            if val is not None:
                setattr(blog, field, val)
        pd = request.POST.get('published_date')
        if pd is not None:
            blog.published_date = pd or None
        if 'author_image' in request.FILES:
            blog.author_image = request.FILES['author_image']
        for file in request.FILES.getlist('attachments'):
            BlogAttachment.objects.create(blog=blog, file=file)

    blog.save()
    return _cors(JsonResponse(serialize_blog(blog, request)))


@csrf_exempt
def delete_blog(request, blog_id):
    if request.method == 'OPTIONS':
        return _cors(JsonResponse({}, status=200))
    if request.method != 'DELETE':
        return _cors(JsonResponse({'error': 'Method not allowed'}, status=405))

    try:
        blog = BlogPost.objects.get(id=blog_id)
    except BlogPost.DoesNotExist:
        return _cors(JsonResponse({'error': 'Blog not found'}, status=404))

    blog.delete()
    return _cors(JsonResponse({'message': 'Blog deleted'}, status=200))
