from django.contrib import admin
from .models import (
UserProfile, Category, Page, CategoryMap, Comment, LikeCategory, LikeComment, LikePage
)
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(CategoryMap)
admin.site.register(Comment)
admin.site.register(LikeCategory)
admin.site.register(LikeComment)
admin.site.register(LikePage)
