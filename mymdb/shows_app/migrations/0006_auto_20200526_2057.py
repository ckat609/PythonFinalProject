# Generated by Django 2.2.4 on 2020-05-27 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows_app', '0005_auto_20200526_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='genre',
            field=models.ManyToManyField(related_name='shows', to='shows_app.Genre'),
        ),
        migrations.AddField(
            model_name='show',
            name='medium',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='runtime',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='total_episodes',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='total_seasons',
            field=models.IntegerField(null=True),
        ),
    ]
