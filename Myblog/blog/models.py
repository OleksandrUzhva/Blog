from django.db import models
from user.models import User

class PostManagers(models.Manager):
    def filter_by_participent(self, user: User):
        return self.filter(user=user)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_blog"
    )

    objects = PostManagers()

    def __repr__(self) -> str:
        return f"Issue[{self.pk} {self.title[:10]}]"

    def __str__(self) -> str:
        return self.title[:10]
    

class Comments(models.Model):
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comment"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comment"
    )