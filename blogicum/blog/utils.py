from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Count


def get_posts(post_objects):
    return post_objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).annotate(comment_count=Count('comments'))


def get_paginator(request, items, num=10):
    paginator = Paginator(items, num)
    num_pages = request.GET.get('page')
    return paginator.get_page(num_pages)
