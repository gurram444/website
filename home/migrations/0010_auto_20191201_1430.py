# Generated by Django 2.2.7 on 2019-12-01 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20191201_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new_portfolio',
            name='profile_pic',
            field=models.ImageField(default=1, upload_to='media/'),
            preserve_default=False,
        ),
    ]