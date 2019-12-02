# Generated by Django 2.2.7 on 2019-12-01 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='New_Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.CharField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50)], max_length=10, verbose_name='Experience')),
                ('qualification', models.CharField(choices=[('UG', 'UNDER GRADUATE'), ('G', 'GRADUATE'), ('PG', 'POST GRADUATE'), ('PhD', 'PhD')], max_length=20, verbose_name='Qualification')),
                ('budget', models.CharField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59), (60, 60), (61, 61), (62, 62), (63, 63), (64, 64), (65, 65), (66, 66), (67, 67), (68, 68), (69, 69), (70, 70), (71, 71), (72, 72), (73, 73), (74, 74), (75, 75), (76, 76), (77, 77), (78, 78), (79, 79), (80, 80), (81, 81), (82, 82), (83, 83), (84, 84), (85, 85), (86, 86), (87, 87), (88, 88), (89, 89), (90, 90), (91, 91), (92, 92), (93, 93), (94, 94), (95, 95), (96, 96), (97, 97), (98, 98), (99, 99), (100, 100)], max_length=20, verbose_name='Budget')),
                ('prefix', models.CharField(choices=[('MR', 'MR'), ('MRS', 'MRS'), ('MS', 'MS'), ('MX', 'MX')], max_length=3, verbose_name='Prefix')),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=10, verbose_name='Gender')),
                ('mobile_phone', models.CharField(max_length=10, null=True, unique=True, verbose_name='Mobile phone')),
                ('secondary_phone', models.CharField(max_length=10, null=True, unique=True, verbose_name='Secondary phone')),
                ('tel_phone', models.CharField(max_length=10, null=True, unique=True, verbose_name='Tele phone')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('about_me', models.CharField(blank=True, max_length=250, verbose_name='About me ')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to=home.models.content_file_name, verbose_name='Profile Picture')),
                ('location', models.CharField(max_length=30, verbose_name='location')),
                ('client', models.BooleanField(default=0, verbose_name='Client')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Category')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Sub_category')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
