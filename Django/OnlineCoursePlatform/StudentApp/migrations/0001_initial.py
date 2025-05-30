# Generated by Django 5.1.7 on 2025-05-06 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enrolled_Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('created_by', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='course_thumbnails/')),
                ('user', models.CharField(max_length=20)),
            ],
        ),
    ]
