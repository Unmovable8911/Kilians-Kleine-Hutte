from django.shortcuts import render, redirect
from music.models import Track, Playlist, MemberShip

# Create your views here.
def admin_set_language(request, object_ids):
    objects = []
    for obj_id in object_ids.split(","):
        objects.append(Track.objects.get(pk=obj_id))

    if request.method == "POST":
        language = request.POST.get("language")
        for obj in objects:
            obj.language = language
            obj.save()

        return redirect("admin:music_track_changelist")

    context = {
        "object_ids": object_ids,
        "objects": objects,
        "num": len(objects),
        "opts": Track._meta
    }
    return render(request, "music/admin_set_language.html", context)

def admin_delete_tracks(request, obj_ids):
    objs = []
    for obj_id in obj_ids.split(","):
        objs.append(Track.objects.get(pk=obj_id))
    
    if request.method == "POST":
        for obj in objs:
            obj.delete()
        return redirect("admin:music_track_changelist")
    
    context = {
        "obj_ids": obj_ids,
        "objs": objs,
        "num": len(objs),
        "opts": Track._meta,
    }

    return render(request, "music/admin_delete_tracks.html", context)

def admin_add_to_playlist(request, obj_ids):
    objs = []
    for obj_id in obj_ids.split(","):
        objs.append(Track.objects.get(pk=obj_id))
    
    pls = Playlist.objects.all()
    
    if request.method == "POST":
        pl_pk = request.POST.get("playlist")
        playlist = Playlist.objects.get(pk=pl_pk)

        for obj in objs:
            memberships = obj.membership_set.all()
            track_pls = []
            for membership in memberships:
                track_pls.append(membership.playlist)
            if playlist not in track_pls:
                new_mem = MemberShip()
                new_mem.playlist = playlist
                new_mem.track = obj
                new_mem.save()

        return redirect("admin:music_track_changelist")
    
    context = {
        "obj_ids": obj_ids,
        "objs": objs,
        "num": len(objs),
        "pls": pls,
        "opts": Track._meta
    }

    return render(request, "music/admin_add_to_playlist.html", context)

def admin_remove_from_playlist(request, obj_ids):
    objs = []
    for obj_id in obj_ids.split(","):
        objs.append(Track.objects.get(pk=obj_id))
    
    pls = set()
    for obj in objs:
        memberships = obj.membership_set.all()
        for membership in memberships:
            pls.add(membership.playlist)

    if request.method == "POST":
        playlist = Playlist.objects.get(pk=request.POST.get("playlist"))
        for obj in objs:
            memberships = obj.membership_set.all()
            for membership in memberships:
                if membership.playlist == playlist:
                    membership.delete()
                else:
                    continue
        return redirect("admin:music_track_changelist")
    
    context = {
        "obj_ids": obj_ids,
        "objs": objs,
        "num": len(objs),
        "pls": pls,
        "opts": Track._meta
    }

    return render(request, "music/admin_remove_from_playlist.html", context)
