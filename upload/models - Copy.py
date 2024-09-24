from django.db import models
from autoslug import AutoSlugField
from imagekit import ImageSpec
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from django.urls import reverse
from django.db.models.signals import post_delete, pre_save, pre_delete
from django.dispatch import receiver
import os
from imagekit import ImageSpec
from imagekit.models import ImageSpecField
from django.core.files.storage import FileSystemStorage
from imagekit.processors import ResizeToFit
from django.core.files.storage import default_storage
from imagekit.cachefiles import ImageCacheFile
from django.core.exceptions import ObjectDoesNotExist


class Tag(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Project(models.Model):
    alt_img_description = models.CharField(max_length=100)
    project_description = models.TextField()
    title = models.CharField(max_length=50)
    service = models.CharField(max_length=50)
    overview = models.TextField(max_length=350)
    size = models.CharField(max_length=10)
    year = models.CharField(max_length=4)
    tags = models.ManyToManyField(Tag)
    location = models.CharField(max_length=70)
    meta_title = models.CharField(max_length=40)
    meta_description = models.CharField(max_length=160)
    meta_keywords = models.CharField(max_length=160)
    project_slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.project_slug)])

def get_upload_path(instance, filename):
    return f'images/{instance.project.title}/{filename}'

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, default=None, on_delete=models.CASCADE)
    original_images_666x420 = models.ImageField(upload_to=get_upload_path)

    thumbnail_300x189 = ImageSpecField(source='original_images_666x420',
                                       processors=[ResizeToFit(300, 189)],
                                       format='JPEG',
                                       options={'quality': 90})
    thumbnail_50x32 = ImageSpecField(source='original_images_666x420',
                                     processors=[ResizeToFit(50, 32)],
                                     format='JPEG',
                                     options={'quality': 90})

    def __str__(self):
        return self.project.title

# Define a function to delete cached thumbnails
def delete_cached_thumbnails(sender, instance, **kwargs):
    # Delete the cached thumbnails using the storage attribute
    instance.thumbnail_300x189.storage.delete(instance.thumbnail_300x189.name)
    instance.thumbnail_50x32.storage.delete(instance.thumbnail_50x32.name)

# Connect the function to the post_delete signal of ProjectImage
post_delete.connect(delete_cached_thumbnails, sender=ProjectImage)

# Define a function to delete related images and thumbnails when a Project is deleted
def delete_project_images(sender, instance, **kwargs):
    # Delete all related ProjectImage objects
    project_images = instance.projectimage_set.all()
    for project_image in project_images:
        # Delete the original image of the ProjectImage
        project_image.original_images_666x420.delete(save=False)

# Connect the function to the post_delete signal of Project
pre_delete.connect(delete_project_images, sender=Project)