# Generated by Django 4.1.2 on 2022-11-23 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0004_comment_global_msg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='global_msg',
        ),
        migrations.AddField(
            model_name='tarefa',
            name='global_msg',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
