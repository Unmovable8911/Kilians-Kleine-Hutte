from django.db import models
from django.urls import reverse
import uuid, os
from datetime import datetime
from PIL import Image
from markdownx.models import MarkdownxField

# Create your models here.
class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    class Meta:
        ordering = ["-publish_date"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=70)
    cover = models.ImageField(upload_to="posts/%Y/%m/")
    body = MarkdownxField()
    publish_date = models.DateField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def _short_title(self):
        if len(self.title) > 45:
            return self.title[:42] + "..."
        else:
            return self.title

    def __str__(self):
        return self._short_title()
        
    def save(self, *args, **kwargs):
        try: # test if the it's the initial save
            # the post already exists
            original = Post.objects.get(pk=self.pk)
            original_cover_path = original.cover.path

            # test if the cover has changed
            if self.cover.path != original_cover_path: # cover changed
                if os.path.exists(original_cover_path):
                    os.remove(original_cover_path) # remove the original cover file
                super().save(*args, **kwargs) # save the new cover
                self._resize_cover() # resize the new cover
            else: # cover not changed
                super().save(*args, **kwargs)

        except self.DoesNotExist: # the post does not exist
            super().save(*args, **kwargs)
            self._resize_cover()

    def _resize_cover(self):
        origi_path = self.cover.path
        cover = Image.open(origi_path) # load the image
        filename = os.path.basename(origi_path)

        # resize the cover
        resized = cover.resize((1500, 857))
        
        resized.save("media/temp/{}".format(filename)) # save to temp
        os.remove(origi_path) # remove the original picture
        with open("media/temp/{}".format(filename), "rb") as f:
            self.cover.save(filename, f)
        os.remove("media/temp/{}".format(filename)) # delete temp picture

        cover.close()
        resized.close()

    # @property
    # def _original_cover_path(self):
    #     try:
    #         if self.pk:
    #             original = Post.objects.get(pk=self.pk)
    #             return original.cover.path
    #         else:
    #             return None
    #     except self.DoesNotExist:
    #         return None
        
    def delete(self, *args, **kwargs):
        # The default delete method won't automatically delete the files
        # attached to the record.
        if self.cover: # make sure the cover exists
            dir_month = os.path.dirname(self.cover.path)
            dir_year = os.path.dirname(dir_month)

            # remove the cover picture
            if os.path.exists(self.cover.path):
                os.remove(self.cover.path)
            
            # remove the directory which contains the picture files if the
            # directory is empty
            for directory in (dir_month, dir_year):
                try:
                    os.rmdir(directory)
                except OSError:
                    break
                else:
                    continue
        
        super().delete(*args, **kwargs)
        
