# Generated by Django 4.1.2 on 2022-11-18 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='helpdesk/covers/%Y/%m/%d/', verbose_name='Foto de perfil'),
        ),
    ]
