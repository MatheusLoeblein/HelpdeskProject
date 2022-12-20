# Generated by Django 4.1.2 on 2022-12-16 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0006_profile_maquina'),
    ]

    operations = [
        migrations.AddField(
            model_name='maquinas',
            name='mac',
            field=models.TextField(blank=True, max_length=17, null=True, verbose_name='MAC'),
        ),
        migrations.AlterField(
            model_name='maquinas',
            name='ativo',
            field=models.BooleanField(default=False, verbose_name='Maquina Ativa'),
        ),
        migrations.AlterField(
            model_name='maquinas',
            name='e7',
            field=models.BooleanField(default=False, verbose_name='E7 Antivirus'),
        ),
        migrations.AlterField(
            model_name='maquinas',
            name='office',
            field=models.BooleanField(default=False, verbose_name='Pacote Office'),
        ),
        migrations.AlterField(
            model_name='maquinas',
            name='usuariofc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authors.usuariofc', verbose_name='Fórmula Certa'),
        ),
    ]