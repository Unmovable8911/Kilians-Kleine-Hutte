from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from markdown import markdown as md
from .models import Post, Topic

# Create your views here.
def _post_list_filter_posts(pks):
    posts = Post.objects.none()
    selected_topics = []
    for pk in pks:
        posts = posts | Post.objects.filter(topic_id=pk)
        selected_topics.append(Topic.objects.get(pk=pk))
    return (posts, selected_topics)

def post_list(request):
    topics = Topic.objects.all().order_by("name")
    selected_topics = []

    get_dict = dict()
    for name, value in request.GET.lists():
        get_dict[name] = value
    
    if not get_dict: # no page and filter
        posts = Post.objects.all()
        page = 1
    elif not get_dict.get("page"): # no page
        (posts, selected_topics) = _post_list_filter_posts(get_dict["topics"])
        page = 1
    elif not get_dict.get("topics"): # page without filter
        posts = Post.objects.all()
        try:
            page = int(get_dict["page"][0])
        except ValueError:
            page = 1
    else: # change page with filtered posts
        (posts, selected_topics) = _post_list_filter_posts(get_dict["topics"])
        print(request.GET)
        try:
            page = int(get_dict["page"][0])
        except ValueError:
            page = 1

    paginator = Paginator(posts, 20)    
    paged_posts = paginator.get_page(page)

    for post in paged_posts:
        short = post.body[:150] + "..."
        post.html_body = md(short, extensions=['markdown.extensions.extra'])
        post.short = post._short_title()
        post.publish_date = post.publish_date.isoformat

    context = {
        "paged_posts": paged_posts,
        "posts": posts,
        "topics": topics,
        "selected_topics": selected_topics
    }
    return render(request, "posts/post_list.html", context)

def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    post.html_body = md(post.body, extensions=["markdown.extensions.extra"])
    context = {"post": post}
    return render(request, "posts/post_detail.html", context)

def admin_delete_posts(request, obj_ids):
    objs = []
    for obj_id in obj_ids.split(","):
        objs.append(Post.objects.get(pk=obj_id))
    
    if request.method == "POST":
        for obj in objs:
            obj.delete()
        
        return redirect("admin:posts_post_changelist")
    
    context = {
        "obj_ids": obj_ids,
        "objs": objs,
        "num": len(objs),
        "opts": Post._meta,
    }

    return render(request, "posts/admin_delete_posts.html", context)
