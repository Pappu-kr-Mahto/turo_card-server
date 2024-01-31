# Generated by Django 4.2.8 on 2024-01-31 04:43

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
            name='SwappingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('senderUser', models.CharField(max_length=100)),
                ('receiverUser', models.CharField(max_length=100)),
                ('senderCard', models.IntegerField(default=0)),
                ('receiverCard', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TuroCards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(null=True, upload_to='images')),
                ('description', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('card_no', models.IntegerField()),
                ('status', models.CharField(choices=[('public', 'public'), ('private', 'private')], max_length=20)),
                ('likes', models.TextField(default=[], verbose_name='[]')),
                ('likes_count', models.IntegerField(default=0)),
                ('comments', models.TextField(default=[], verbose_name='[]')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
