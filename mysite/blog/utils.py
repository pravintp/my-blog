from django.core.mail import send_mail


def share_post_by_email(post, name, share_text, to_mail):
    post_url = post.get_absolute_uri(post.get_absolute_url())
    subject = f"{name} recommends you read {post.title}"
    message = f"Read {post.title} at {post_url}\n\n {name}'s says: {share_text}"
    send_mail(subject, message, "admin@myblog.com", to_mail)