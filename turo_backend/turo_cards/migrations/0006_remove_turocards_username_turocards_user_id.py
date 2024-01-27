# Generated by Django 4.2.8 on 2024-01-12 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('turo_cards', '0005_turocards_comments_turocards_likes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turocards',
            name='username',
        ),
        migrations.AddField(
            model_name='turocards',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
