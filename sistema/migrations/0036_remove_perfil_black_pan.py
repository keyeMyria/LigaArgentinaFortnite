# Generated by Django 2.1.1 on 2018-11-09 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0035_auto_20181109_1650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='black_pan',
        ),
    ]
