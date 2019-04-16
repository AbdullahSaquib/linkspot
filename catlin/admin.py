from django.contrib import admin
from .models import (
    Category, Page, Comment, LikeCategory, LikeComment, LikePage
)
# Register your models here.
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(Comment)
admin.site.register(LikeCategory)
admin.site.register(LikeComment)
admin.site.register(LikePage)
