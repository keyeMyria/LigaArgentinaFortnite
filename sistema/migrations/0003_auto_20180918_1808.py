# Generated by Django 2.1.1 on 2018-09-18 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0002_perfil_twitch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='apellido',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='nombre',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='plataforma',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='twitch',
            field=models.CharField(max_length=20),
        ),
    ]
