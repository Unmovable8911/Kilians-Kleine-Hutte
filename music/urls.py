from django.urls import path
from music.views import (
    admin_set_language,
    admin_delete_tracks,
    admin_add_to_playlist,
    admin_remove_from_playlist,
)

urlpatterns = [
    path(
        "admin/music/track/set-language?<str:object_ids>",
        admin_set_language,
        name="admin_set_language",
    ),
    path(
        "admin/music/track/delete-tracks?<str:obj_ids>",
        admin_delete_tracks,
        name="admin_delete_tracks",
    ),
    path(
        "admin/music/track/add-to-playlist?<str:obj_ids>",
        admin_add_to_playlist,
        name="admin_add_to_playlist"
    ),
    path(
        "admin/music/track/remove-from-playlist?<str:obj_ids>",
        admin_remove_from_playlist,
        name="admin_remove_from_playlist"
    ),
]
