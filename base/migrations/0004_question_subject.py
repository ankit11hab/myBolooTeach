# Generated by Django 3.2.7 on 2021-12-07 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_question_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.CharField(default='', max_length=100),
        ),
    ]