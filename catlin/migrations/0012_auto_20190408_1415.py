# Generated by Django 2.1.7 on 2019-04-08 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catlin', '0011_auto_20190408_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
