from django.shortcuts import render

from .models import Post


def post_list(request):
    return render(request, "blog/post/list.html", {"posts": Post.published.all()})
