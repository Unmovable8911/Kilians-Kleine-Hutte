from django.db import models
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
import os, uuid, random, eyed3, json

# Create your models here.
class Playlist(models.Model):
    class Meta:
        ordering = ["name"]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

def upload_dir(inst, filename):
    dirname = "music/track"
    name = str(random.randint(0, 9999)).zfill(4)
    extension = filename.split(".")[-1]

    # determine path with tree-status.json
    with open("media/music/tree-status.json", "r") as f:
        root = json.load(f)

    base_name = root["not_full_dirs"][0]
    base = root["dirs"][base_name]
    child_name = base["not_full_dirs"][0]
    
    return f'{dirname}/{base_name}/{child_name}/{name}.{extension}'

def album_art_upload_dir(inst, filename):
    path = upload_dir(inst, filename)
    path = path[:6] + "album-art" + path[11:]
    return path

class Track(models.Model):
    class Meta:
        ordering = ["-upload_time"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    music_file = models.FileField(upload_to=upload_dir)

    # music metadata
    title = models.CharField(max_length=100, blank=True, null=True, default="Unknow")
    album = models.CharField(max_length=100, blank=True, null=True, default="Unknow")
    artist = models.CharField(max_length=100, blank=True, null=True, default="Unknow")
    album_art = models.ImageField(upload_to=album_art_upload_dir, blank=True, null=True, default="Unknow")
    language = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=[
            ("EN", "English"),
            ("CN", "中文"),
            ("DU", "Deutcher"),
            ("FR", "Français"),
            ("IT", "Italiano"),
            ("SP", "Español"),
            ("RU", "Pусский"),
            ("JP", "日本語"),
            ("KR", "한국어"),
            ("NO", "Instrumental")
        ]
    )
    lyrics = models.TextField(blank=True, null=True)
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def _update_tree_status(self, option):
        with open("media/music/tree-status.json", "r") as f:
            tree_status = json.load(f)
        path = self.music_file.path
        path_as_li = path.split("/")
        child = path_as_li[-2]
        base = path_as_li[-3]

        if option == "add":
            tree_status["dirs"][base]["dirs"][child] += 1
            if tree_status["dirs"][base]["dirs"][child] == 50:
                tree_status["dirs"][base]["not_full_dirs"].remove(child)
                if len(tree_status["dirs"][base]["not_full_dirs"]) == 0:
                    tree_status["not_full_dirs"].remove(base)
        if option == "del":
            tree_status["dirs"][base]["dirs"][child] -= 1
            if tree_status["dirs"][base]["dirs"][child] == 49:
                tree_status["dirs"][base]["not_full_dirs"].append(child)
                tree_status["dirs"][base]["not_full_dirs"].sort()
                if base not in tree_status["not_full_dirs"]:
                    tree_status["not_full_status"].append(base)
                    tree_status["not_full_status"].sort()

        with open("media/music/tree-status.json", "w") as f:
            tree_status = json.dump(tree_status, f, indent=2)

    def _get_id3(self):
        mp3 = eyed3.load(self.music_file.path)
        self.title = mp3.tag.title
        self.album = mp3.tag.album
        self.artist = mp3.tag.artist
        self.lyrics = mp3.tag.lyrics[0].text

        # extract cover image
        image_data = mp3.tag.images[0].image_data
        image_file = ImageFile(ContentFile(image_data), name="cover.jpg")
        self.album_art = image_file

        # clear the metadata of the music file
        mp3.tag.clear()
        mp3.tag.save()

    def save(self, *args, **kwargs):
        try:
            original = Track.objects.get(pk=self.pk)
            # Updating the record
            super().save(*args, **kwargs)
        except self.DoesNotExist: # Creating of the record
            super().save(*args, **kwargs)
            self._get_id3()
            self._update_tree_status("add")
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        def clean(path: str):
            dir_child = os.path.dirname(path)
            dir_base = os.path.dirname(dir_child)
            if os.path.exists(path):
                os.remove(path)

            for directory in (dir_child, dir_base):
                try:
                    os.rmdir(directory)
                except OSError:
                    break
                else:
                    continue

        if self.music_file:
            clean(self.music_file.path)
        if self.album_art:
            clean(self.album_art.path)

        super().delete(*args, **kwargs)
        self._update_tree_status("del")

class MemberShip(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
