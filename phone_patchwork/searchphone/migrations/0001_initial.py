# Generated by Django 2.1.5 on 2019-02-05 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=20, unique=True)),
                ('id_42', models.IntegerField(unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('mail', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=250)),
                ('detail_url', models.CharField(max_length=250, unique=True)),
                ('intra_url', models.CharField(max_length=250)),
            ],
        ),
    ]