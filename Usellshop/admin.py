from django.contrib import admin
from .models import Course,Tag,Learning,Video,Prerequisite,Module,UserCourse,Payment,Copun
# Register your models here.

class TagAdmin(admin.TabularInline):
    model=Tag

class PrerequisiteAdmin(admin.TabularInline):
    model=Prerequisite

class LearningAdmin(admin.TabularInline):
    model=Learning

class VideoAdmin(admin.TabularInline):
    model=Video


class CourseAdmin(admin.ModelAdmin):
    inlines=[TagAdmin,PrerequisiteAdmin,LearningAdmin,VideoAdmin]


admin.site.register(Course,CourseAdmin)
admin.site.register(Module)
admin.site.register(UserCourse)
admin.site.register(Payment)
admin.site.register(Copun)