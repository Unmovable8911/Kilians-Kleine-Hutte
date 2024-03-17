from django.contrib import admin
from django.db import models
from django.utils.html import mark_safe
from markdownx.admin import MarkdownxModelAdmin
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Post, Topic

class PostInline(admin.TabularInline):
    model = Post
    extra = 1
    exclude = ["body"]

class PostAdmin(MarkdownxModelAdmin):
    class Media:
        # Assets definition
        css = {
            "all": ["admin/music/changelist.css"],
        }

    list_display = ["display_cover", "title", "publish_date", "topic", "edit_link"]
    date_hierarchy = "publish_date"
    list_display_links = ["edit_link"]
    list_per_page = 50
    search_fields = ["title", "body", "topic__name"]
    list_filter = ["topic__name", "publish_date"]

    fields = [("title", "topic"), "cover", "body"]
    actions = ["bulk_delete"]

    @admin.display(description="")
    def edit_link(self, instance):
        return mark_safe(
            """
            <span style='
                background-color: #e4e3e3;
                padding: 0.2em;
                '>Edit</span>
            """)

    @admin.display(description="COVER")
    def display_cover(self, instance):
        if instance.cover:
            return mark_safe('<img src="{}" width="200" height="114">'.format(instance.cover.url))
        else:
            return None
    
    @admin.action(description="Delete Posts")
    def bulk_delete(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        obj_ids = ",".join(str(pk) for pk in selected)
        return HttpResponseRedirect(
            reverse("admin_delete_posts", kwargs={"obj_ids": obj_ids})
        )
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

class TopicAdmin(admin.ModelAdmin):
    inlines = [PostInline]
    class Media:
        # Assets definition
        css = {
            "all": ["admin/music/changelist.css"],
        }

    search_fields = ["name"]
    list_per_page = 50
    list_display = ["name", "edit_link"]
    list_display_links = ["edit_link"]

    @admin.display(description="")
    def edit_link(self, inst):
        return mark_safe(
            """
            <span style='
                background-color: #e4e3e3;
                padding: 0.2em;
                '>Edit</span>
            """)
# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Topic, TopicAdmin)
