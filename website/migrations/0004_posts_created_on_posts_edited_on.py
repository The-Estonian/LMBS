# Generated by Django 4.0.4 on 2022-07-06 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_alter_templates_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default='2000-01-01 00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='edited_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]