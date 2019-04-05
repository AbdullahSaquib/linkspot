# Generated by Django 2.1.7 on 2019-03-30 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('summary', models.CharField(max_length=500)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('category_has_cat', models.BooleanField(default=False)),
                ('views', models.PositiveIntegerField(default=0)),
                ('like_count', models.PositiveIntegerField(default=0)),
                ('dislike_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
            },
        ),
        migrations.CreateModel(
            name='CategoryMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_in_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='catlin.Category')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='catlin.Category')),
            ],
            options={
                'verbose_name_plural': 'Categories map',
                'verbose_name': 'Category map',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('like_count', models.PositiveIntegerField(default=0)),
                ('dislike_count', models.PositiveIntegerField(default=0)),
                ('depth', models.CharField(choices=[('M', 'Main Comment'), ('N', 'Nested Comment')], default='M', max_length=1)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catlin.Category')),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catlin.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='LikeCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('L', 'Like'), ('D', 'Dislike')], max_length=1)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catlin.Category')),
            ],
            options={
                'verbose_name_plural': 'Like categories',
                'verbose_name': 'Like category',
            },
        ),
        migrations.CreateModel(
            name='LikeComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('L', 'Like'), ('D', 'Dislike')], max_length=1)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catlin.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='LikePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('L', 'Like'), ('D', 'Dislike')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('summary', models.CharField(max_length=500)),
                ('url', models.URLField()),
                ('views', models.PositiveIntegerField(default=0)),
                ('like_count', models.PositiveIntegerField(default=0)),
                ('dislike_count', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catlin.Category')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='profile_pictures')),
                ('category_count', models.PositiveIntegerField(default=0)),
                ('like_count', models.PositiveIntegerField(default=0)),
                ('dislike_count', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='likepage',
            name='entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catlin.Page'),
        ),
        migrations.AddField(
            model_name='likepage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catlin.UserProfile'),
        ),
        migrations.AddField(
            model_name='likecomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catlin.UserProfile'),
        ),
        migrations.AddField(
            model_name='likecategory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catlin.UserProfile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catlin.UserProfile'),
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catlin.UserProfile'),
        ),
        migrations.AddIndex(
            model_name='page',
            index=models.Index(fields=['category', 'title'], name='catlin_page_categor_ba5adf_idx'),
        ),
        migrations.AddIndex(
            model_name='likepage',
            index=models.Index(fields=['entity'], name='catlin_like_entity__d03d62_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='likepage',
            unique_together={('user', 'entity')},
        ),
        migrations.AddIndex(
            model_name='likecomment',
            index=models.Index(fields=['entity'], name='catlin_like_entity__1eba18_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='likecomment',
            unique_together={('user', 'entity')},
        ),
        migrations.AddIndex(
            model_name='likecategory',
            index=models.Index(fields=['entity'], name='catlin_like_entity__5e2a88_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='likecategory',
            unique_together={('user', 'entity')},
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['category'], name='catlin_comm_categor_0b8dde_idx'),
        ),
        migrations.AddIndex(
            model_name='categorymap',
            index=models.Index(fields=['category'], name='catlin_cate_categor_200d72_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='categorymap',
            unique_together={('category', 'cat_in_category')},
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['title'], name='catlin_cate_title_40d3aa_idx'),
        ),
    ]
