# Generated by Django 4.0 on 2022-01-27 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disparate_times', '0004_alter_word_word'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='rel_word',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='word',
            name='word',
            field=models.CharField(max_length=100),
        ),
    ]
