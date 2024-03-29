# Generated by Django 2.2.4 on 2019-09-11 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=15)),
                ('description', models.CharField(max_length=5000)),
                ('lang', models.CharField(max_length=10)),
                ('url', models.CharField(max_length=200, unique=True)),
                ('published', models.BooleanField(blank=True, default=True)),
                ('active', models.BooleanField(blank=True, default=True)),
            ],
            options={
                'permissions': (('select_site', 'Select site.'), ('manage_site', 'Manage site.')),
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=15)),
                ('description', models.CharField(max_length=5000)),
                ('lang', models.CharField(max_length=10)),
                ('url', models.CharField(max_length=200, unique=True)),
                ('published', models.BooleanField(blank=True, default=True)),
                ('active', models.BooleanField(blank=True, default=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Site')),
            ],
            options={
                'permissions': (('select_feed', 'Select feed.'), ('manage_feed', 'Manage feed.')),
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('picture_url', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(max_length=5000)),
                ('authors', models.CharField(blank=True, max_length=100)),
                ('url', models.CharField(max_length=200, unique=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('reg_date', models.DateTimeField(auto_now_add=True, verbose_name='date registered')),
                ('published', models.BooleanField(default=True)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Feed')),
            ],
            options={
                'permissions': (('select_article', 'Select article.'), ('manage_article', 'Manage article.')),
                'ordering': ['-reg_date', '-pub_date'],
            },
        ),
    ]
