# Generated by Django 4.1.2 on 2022-11-25 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0006_tasktipe_alter_tarefa_global_msg_alter_tarefa_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Local')),
            ],
        ),
        migrations.AddField(
            model_name='tarefa',
            name='local',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='helpdesk.location', verbose_name='Local'),
        ),
    ]
