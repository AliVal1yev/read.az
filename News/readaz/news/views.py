from django.shortcuts import render, get_object_or_404
from. models import New, Category
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


def home_view(request):
    posts = New.objects.order_by('-created_at')
    catigories = Category.objects.all()
    posts_list = []
    for post in posts:
        post.check_and_expire()
        if post.available == True:
            posts_list.append(post)
        paginator = Paginator(posts_list, 5)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
    context = {
        'posts':posts,
        'catigories': catigories
    }
    return render(request, 'news/home.html', context)


def post_detail(requset, id):
    post = New.objects.get(id=id)
    post.watch_count += 1
    post.save(update_fields=['watch_count'])
    
    context = {
        'post':post
    }
    return render (requset, 'news/details.html', context)


@csrf_exempt
def like_post(request, post_id):
    if request.method == 'POST':
        session_key = request.session.session_key or request.session.create()
        post = New.objects.get(id=post_id)

        interaction_key = f'like_{post_id}'
        if request.session.get(interaction_key):
            post.likes -= 1
            request.session.pop(interaction_key)
        else:
            post.likes += 1
            request.session[interaction_key] = True

        post.save()
        return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})

@csrf_exempt
def dislike_post(request, post_id):
    if request.method == 'POST':
        session_key = request.session.session_key or request.session.create()
        post = New.objects.get(id=post_id)

        interaction_key = f'dislike_{post_id}'
        if request.session.get(interaction_key):
            post.dislikes -= 1
            request.session.pop(interaction_key)
        else:
            post.dislikes += 1
            request.session[interaction_key] = True

        post.save()
        return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})
    
    
    
def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = New.objects.filter(category=category)
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'news/category.html', context)