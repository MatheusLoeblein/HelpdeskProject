# Generated by Django 4.1.2 on 2022-10-31 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarefa',
            name='Category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='helpdesk.category'),
        ),
    ]