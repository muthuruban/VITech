# Generated by Django 4.2.3 on 2023-08-10 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='date_Ofjoin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='date_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='mail_id',
            field=models.EmailField(max_length=40),
        ),
    ]
