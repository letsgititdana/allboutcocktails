# Generated by Django 3.1 on 2020-09-04 03:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wineapp', '0002_post_cocktailapi'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cocktailCategory',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='cocktailInst',
            field=models.CharField(default=django.utils.timezone.now, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='cocktailAPI',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='post',
            name='cocktailName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='cocktailPic',
            field=models.CharField(max_length=200),
        ),
    ]
