from django.db import models
from autoslug import AutoSlugField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from django.urls import reverse
from django.db.models.signals import post_delete, pre_save, pre_delete
import os
from imagekit import ImageSpec
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from django.utils.text import slugify
from django.conf import settings
import fitz  # Import PyMuPDF
from io import BytesIO
from PIL import Image



class Tag(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Project(models.Model):
    alt_img_description = models.CharField(max_length=100, help_text="Enter alternative image description for accessibility (alt text)")
    project_description = models.TextField(help_text="Enter the project description")
    title = models.CharField(max_length=50, help_text="Enter the project title")
    service = models.CharField(max_length=50, help_text="Enter the service associated with this project (e.g., residential,commercial or retail)")
    overview = models.TextField(max_length=350, help_text="Enter a brief overview of the project")
    size = models.CharField(max_length=10, help_text="Enter the project size (e.g., 100 sqm, 2000 sqft)")
    year = models.CharField(max_length=4, help_text="Enter the year when the project was completed")
    tags = models.ManyToManyField(Tag, help_text="Create or Select tags related to this project(e.g., construction, architecture, interior design)")
    location = models.CharField(max_length=70, help_text="Enter the project location")
    meta_title = models.CharField(max_length=40, help_text="Enter the meta title for SEO purposes (max 40 characters)")
    meta_description = models.CharField(max_length=160, help_text="Enter the meta description for SEO purposes (max 160 characters)")
    meta_keywords = models.CharField(max_length=160, help_text="Enter the meta keywords for SEO purposes (max 160 characters)")
    project_slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None, help_text="Automatically generated slug for the project URL")

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
    delete_empty_folders(os.path.join('media', 'cache'))

# Connect the function to the post_delete signal of ProjectImage
post_delete.connect(delete_cached_thumbnails, sender=ProjectImage)

# Define a function to delete related images and thumbnails when a Project is deleted
def delete_project_images(sender, instance, **kwargs):
    # Delete all related ProjectImage objects
    project_images = instance.projectimage_set.all()
    for project_image in project_images:
        # Delete the original image of the ProjectImage
        project_image.original_images_666x420.delete(save=False)
    delete_empty_folders(os.path.join('media', 'images', instance.title))

# Connect the function to the post_delete signal of Project
pre_delete.connect(delete_project_images, sender=Project)

# Define a function to delete empty folders recursively
def delete_empty_folders(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            contents = os.listdir(path)
            for item in contents:
                item_path = os.path.join(path, item)
                delete_empty_folders(item_path)
            if not os.listdir(path):
                os.rmdir(path)

class Contact(models.Model):
    COMPANY_CHOICES = [
        ('vastukar_architects', 'Vastukar Architects'),
        ('vastukar_interior', 'Vastukar Interior Designs'),
        ('certified_construction', 'Certified Construction Services'),
    ]

    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, choices=COMPANY_CHOICES)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    message = models.TextField()
    agree = models.BooleanField()

    def __str__(self):
        return self.name
    



class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    date_uploaded = models.DateField()
    pdf_file = models.FileField(upload_to='pdfs/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        if not self.thumbnail:
            pdf_path = self.pdf_file.path
            images = self.pdf_page_to_image(pdf_path)

            if images:
                thumbnail_path = pdf_path.replace('.pdf', '.jpg')
                thumbnail_image = images[0]
                # Resize the thumbnail to a smaller size while maintaining aspect ratio
                thumbnail_image.thumbnail((400, 400))  # Adjust the dimensions as needed
                thumbnail_image.save(thumbnail_path, format='JPEG')

                self.thumbnail.name = os.path.relpath(thumbnail_path, settings.MEDIA_ROOT)
                super().save(*args, **kwargs)

    def pdf_page_to_image(self, pdf_path):
        img_temp = BytesIO()

        pdf_document = fitz.open(pdf_path)  # Open the PDF document
        pdf_page = pdf_document[0]  # Get the first page

        pix = pdf_page.get_pixmap()  # Get a pixmap from the page
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        pdf_document.close()  # Close the PDF document

        return [img]

    def delete(self, *args, **kwargs):
        print("Delete method called")

        if self.thumbnail:
            storage, thumbnail_path = self.thumbnail.storage, self.thumbnail.path
            storage.delete(thumbnail_path)
        super().delete(*args, **kwargs)