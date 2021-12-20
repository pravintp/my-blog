from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages

from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm
from .utils import share_post_by_email, get_search_results


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.save()
            return render(
                request,
                "blog/post/detail.html",
                {
                    "post": post,
                    "comment_form": comment_form,
                },
            )

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comment_form": CommentForm(initial={"post": post.id}),
        },
    )


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            share_post_by_email(
                post,
                form.cleaned_data["name"],
                form.cleaned_data["share_text"],
                form.cleaned_data["to"],
            )
            messages.success(
                request, f"{post.title} was successfully sent to {form.to}"
            )
            return render(request, "blog/post/share.html", {"post": post, "form": form})

        messages.error(request, "Error sending mail")
        return render(request, "blog/post/share.html", {"post": post, "form": form})

    form = EmailPostForm()
    return render(request, "blog/post/share.html", {"post": post, "form": form})


def post_search(request):
    form = SearchForm()
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            results = get_search_results(form.cleaned_data["query"])
            return render(
                request,
                "blog/post/search.html",
                {"form": form, "results": results},
            )
    return render(request, "blog/post/search.html", {"form": form})
