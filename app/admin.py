from django.contrib import admin
from .models import *


class TopicAdmin(admin.ModelAdmin):
    list_filter = ['language']

class CodeSnippetsAdmin(admin.ModelAdmin):
    list_filter = ['topic']

admin.site.register(Todo)
admin.site.register(User)
admin.site.register(Blogs)
admin.site.register(TutorialName)
admin.site.register(TutorialPost)
admin.site.register(Meme)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(CodeSnippet,CodeSnippetsAdmin)
admin.site.register(Language)
admin.site.register(Contact)
admin.site.register(Comment_tutorials)
admin.site.register(Problem_solve)
admin.site.register(Topics,TopicAdmin)
