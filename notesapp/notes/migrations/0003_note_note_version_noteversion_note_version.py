# Generated by Django 5.0.2 on 2024-02-20 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_noteversion_made_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='note_version',
            field=models.PositiveBigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='noteversion',
            name='note_version',
            field=models.PositiveBigIntegerField(default=11),
            preserve_default=False,
        ),
    ]
