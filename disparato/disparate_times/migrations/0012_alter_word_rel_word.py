# Generated by Django 4.0 on 2022-02-05 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disparate_times', '0011_remove_word_rel_score_alter_word_rel_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='rel_word',
            field=models.JSONField(default='{"word": "time", "score": "1000"}'),
        ),
    ]