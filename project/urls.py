"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# the home page requirements
from django.views import View
from django.shortcuts import render
import os
from project.settings import BASE_DIR
from posts.models import Post
from music.models import Track

class HomePageView(View):
    all_posts = Post.objects.all().order_by("-publish_date")
    posts = all_posts[:6]
    for post in posts:
        post.short = post._short_title()

    context = {
        "posts": posts,
    }

    def get(self, request):
       return render(request, "home.html", self.context)

def search_view(request):
    query = request.GET.get("query", "")
    keywords = query.split(" ")

    posts = []
    tracks = []
    for keyword in keywords:
        posts.append(Post.objects.filter(
            title__icontains = keyword
        ) | Post.objects.filter(
            topic__name__icontains = keyword
        ))
        tracks.append(Track.objects.filter(
            title__icontains = keyword
        ) | Track.objects.filter(
            album__icontains = keyword
        ) | Track.objects.filter(
            artist__icontains = keyword
        ))

    context = {
        "posts": posts,
        "tracks": tracks,
    }
    return render(request, "search.html", context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", HomePageView.as_view(), name="home"),
    path("search/", search_view, name="search"),
    path("blog/", include("posts.urls")),
    path("music/", include("music.urls")),
    path("markdownx/", include("markdownx.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
