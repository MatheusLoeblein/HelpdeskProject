# Generated by Django 4.1.2 on 2022-11-07 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0006_rename_tarefa_comment_tarefa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarefa',
            name='status',
            field=models.CharField(choices=[('A', 'Aberto'), ('E', 'Em Andamento'), ('F', 'Fechado')], max_length=1),
        ),
    ]
