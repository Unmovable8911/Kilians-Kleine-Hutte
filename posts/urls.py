from django.urls import path
from .views import (
    post_list,
    post_detail,
    admin_delete_posts,
)

urlpatterns = [
    # path("post_detail/<int:id>", post_detail, name="post_detail"),
    path("", post_list, name="post_list"),
    path("detail/<uuid:post_pk>", post_detail, name="post_detail"),
    path(
        "admin/posts/post/delete-posts?<str:obj_ids>",
        admin_delete_posts,
        name="admin_delete_posts",
    ),
]