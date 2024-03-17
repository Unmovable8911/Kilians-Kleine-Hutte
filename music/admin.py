from django.contrib import admin
from django.utils.html import mark_safe
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Track, Playlist, MemberShip

class MemberShipInline(admin.TabularInline):
    model = MemberShip
    extra = 1

class TrackAdmin(admin.ModelAdmin):
    class Media:
        # Assets definition
        css = {
            "all": ["admin/music/changelist.css"],
        }
        js = ["admin/music/autoFillFields.js"]

    search_fields = ["title", "artist", "album"]
    list_per_page = 50
    list_filter = ["language", "artist", "album"]
    list_display = [
        "display_album_art",
        "title", "album",
        "artist",
        "language",
        "playlists",
        "edit_link",
        ]
    list_display_links = ["edit_link"]
    inlines = [MemberShipInline]
    actions = ["bulk_delete", "set_language", "add_to_playlist", "remove_from_playlist"]

    # ============display filds=============
    @admin.display(description="Album Art")
    def display_album_art(self, inst):
        if inst.album_art:
            return mark_safe(f'<img src="{inst.album_art.url}">')
        else:
            return None
    
    @admin.display(description="")
    def edit_link(self, inst):
        return mark_safe(
            """
            <span style='
                background-color: #e4e3e3;
                padding: 0.2em;
                '>Edit</span>
            """)

    @admin.display(description="Playlists")
    def playlists(self, inst):
        memberships = inst.membership_set.all()
        playlists_as_html = ""

        for membership in memberships:
            playlists_as_html += "<li>{};</li>".format(str(membership.playlist))
        playlists_as_html = "<ul>" + playlists_as_html + "</ul>"
        return mark_safe(playlists_as_html)

    # ============Actions===============
    @admin.action(description="Delete Tracks")
    def bulk_delete(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        obj_ids = ",".join(str(pk) for pk in selected)
        return HttpResponseRedirect(
            reverse("admin_delete_tracks", kwargs={"obj_ids": obj_ids})
        )

    @admin.action(description="Set Language")
    def set_language(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        object_ids = ",".join(str(pk) for pk in selected)
        return HttpResponseRedirect(
            reverse("admin_set_language", kwargs={"object_ids": object_ids})
        )
    @admin.action(description="Add to Playlist")
    def add_to_playlist(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        obj_ids = ",".join(str(pk) for pk in selected)
        return HttpResponseRedirect(
            reverse("admin_add_to_playlist", kwargs={"obj_ids": obj_ids})
        )
    @admin.action(description="Remove From Playlist")
    def remove_from_playlist(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        obj_ids = ",".join(str(pk) for pk in selected)
        return HttpResponseRedirect(
            reverse("admin_remove_from_playlist", kwargs={"obj_ids": obj_ids})
        )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

class PlaylistAdmin(admin.ModelAdmin):
    inlines = [MemberShipInline]
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


admin.site.register(Track, TrackAdmin)
admin.site.register(Playlist, PlaylistAdmin)
#admin.site.disable_action("delete_selected")
