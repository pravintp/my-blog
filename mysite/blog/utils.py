from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity

from .models import Post


def share_post_by_email(post, name, share_text, to_mail):
    post_url = post.get_absolute_uri(post.get_absolute_url())
    subject = f"{name} recommends you read {post.title}"
    message = f"Read {post.title} at {post_url}\n\n {name}'s says: {share_text}"
    send_mail(subject, message, "admin@myblog.com", to_mail)


def get_search_results(query):
    search_vector = SearchVector("title", "body")
    search_query = SearchQuery(query)
    return (
        Post.published.annotate(
            search=search_vector, rank=SearchRank(search_vector, search_query),
            similarity=TrigramSimilarity("title", query),
        )
        .filter(search=search_query, similarity_gt=0.1)
        .order_by("-rank", "-similarity")
    )
