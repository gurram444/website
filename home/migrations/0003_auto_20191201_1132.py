# Generated by Django 2.2.7 on 2019-12-01 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_new_portfolio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='new_portfolio',
            name='category',
        ),
        migrations.RemoveField(
            model_name='new_portfolio',
            name='sub_category',
        ),
        migrations.RemoveField(
            model_name='new_portfolio',
            name='user',
        ),
    ]
