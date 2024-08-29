from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .utils import get_posts, get_paginator, is_post_author, is_comment_author
from .models import Post, Category, Comment, User
from .forms import PostForm, ProfileEditForm, CommentForm


def index(request):
    post_list = get_posts(Post.objects).order_by('-pub_date')
    page_obj = get_paginator(request, post_list)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    posts = get_object_or_404(Post, id=post_id)
    if request.user != posts.author:
        posts = get_object_or_404(get_posts(Post.objects), id=post_id)
    comments = posts.comments.order_by('created_at')
    form = CommentForm()
    context = {'post': posts, 'form': form, 'comments': comments}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True)
    post_list = get_posts(category.posts).order_by('-pub_date')
    page_obj = get_paginator(request, post_list)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/category.html', context)


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', request.user)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts_list = (
        user.posts
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )
    page_obj = get_paginator(request, posts_list)
    context = {'profile': user, 'page_obj': page_obj}
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    form = ProfileEditForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user)
    context = {'form': form}
    return render(request, 'blog/user.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    redirect_response = is_post_author(request, post)
    if redirect_response:
        return redirect_response

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)

    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    redirect_response = is_post_author(request, post)
    if redirect_response:
        return redirect_response
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', {'post': post})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('blog:post_detail', post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author:
        return redirect('blog:post_detail', post_id)

    form = CommentForm(request.POST or None, instance=comment)

    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)

    context = {'form': form, 'comment': comment}
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    redirect_response = is_comment_author(request, comment, post_id)
    if redirect_response:
        return redirect_response
    if request.method == "POST":
        comment.delete()
        return redirect('blog:post_detail', post_id)
    context = {'comment': comment}
    return render(request, 'blog/comment.html', context)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)
