# Generated by Django 2.1.7 on 2019-04-01 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catlin', '0006_category_page_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_has_cat',
        ),
        migrations.AddField(
            model_name='category',
            name='category_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
