# Generated by Django 4.1.2 on 2022-11-19 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0002_profile_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='cover',
        ),
        migrations.AddField(
            model_name='profile',
            name='cover_profile',
            field=models.ImageField(blank=True, null=True, upload_to='helpdesk/profile/imgs/%Y/%m/%d/', verbose_name='Foto de perfil'),
        ),
    ]
