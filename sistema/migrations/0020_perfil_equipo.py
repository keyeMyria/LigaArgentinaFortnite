# Generated by Django 2.1.1 on 2018-09-26 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0019_remove_perfil_verificado'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='equipo',
            field=models.CharField(blank=True, default=0, max_length=20),
        ),
    ]
