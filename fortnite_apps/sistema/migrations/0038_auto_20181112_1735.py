# Generated by Django 2.1.1 on 2018-11-12 20:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0037_perfil_black_pan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='telefono',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="El telefono tiene que ser ingresado con el formato: '+999999999'", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]