# Generated by Django 2.1.1 on 2018-09-20 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0011_auto_20180920_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='puntos',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
