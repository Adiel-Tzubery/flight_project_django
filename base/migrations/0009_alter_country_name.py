# Generated by Django 4.1.7 on 2023-07-17 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_rename_profile_piq_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
    ]