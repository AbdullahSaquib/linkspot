from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
like_types = (('L','Like'),('D','Dislike')) #for removing like after liking delete the row
comment_types = (('M', 'Main Comment'), ('N','Nested Comment'))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pictures', blank=True)
    category_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=500)
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    last_modified = models.DateTimeField(auto_now_add = True)
    views = models.PositiveIntegerField(default=0)
    category_count = models.PositiveIntegerField(default=0)
    page_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['title',]),
        ]

class Page(models.Model):
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=500)
    url = models.URLField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title
    class Meta:
        indexes = [
            models.Index(fields=['category','title',]),
        ]

class CategoryMap(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='parent') #parent
    cat_in_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='child') #child
    def save(self, *args, **kwargs):
        if self.category.category_count:
            if self.category == self.cat_in_category:
                raise Exception('The recursion is not allowed')
        else:
            self.category.category_count += 1
            self.category.save()
        super(CategoryMap, self).save(*args, **kwargs)
    class Meta:
        unique_together = ('category','cat_in_category')
        verbose_name = 'Category map'
        verbose_name_plural = 'Categories map'
        indexes = [
            models.Index(fields=['category',]),
        ]

class Comment(models.Model):
    content = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    depth = models.CharField(max_length=1, choices=comment_types, default='M')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    comment_count = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.user.user.username +"'s "+self.depth+" comment on "+ self.category.title +" : "+ self.content[:10] +"..."
    class Meta:
        indexes = [
            models.Index(fields=['category',]),
        ]

class LikeCategory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    entity = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=like_types)
    def __str__(self):
        return self.user.user.username+ " " + self.type +" "+ self.entity.title
    class Meta:
        unique_together = (('user', 'entity'))
        verbose_name = 'Like category'
        verbose_name_plural = 'Like categories'
        indexes = [
            models.Index(fields=['entity',]),
        ]

class LikeComment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    entity = models.ForeignKey(Comment, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=like_types)
    def __str__(self):
        return self.user.user.username +" "+ self.type +" a comment on "+ self.entity.category.title
    class Meta:
        unique_together = (('user', 'entity'))
        indexes = [
            models.Index(fields=['entity',]),
        ]

class LikePage(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    entity = models.ForeignKey(Page, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=like_types)
    def __str__(self):
        return self.user.user.username+ " " + self.type +" "+ self.entity.title
    class Meta:
        unique_together = (('user', 'entity'))
        indexes = [
            models.Index(fields=['entity',]),
        ]
    #created_at = models.DateTimeField(auto_now_add = True)
