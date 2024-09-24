from django.contrib import admin
from .models import Project, ProjectImage, Tag, News

class ProjectImageAdmin(admin.StackedInline):
    model = ProjectImage

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageAdmin]

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

from .models import Contact

admin.site.register(Contact)
admin.site.register(News)