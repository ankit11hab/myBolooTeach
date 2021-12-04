# Generated by Django 3.1.2 on 2021-12-04 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('classs', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('paper_file', models.FileField(upload_to='uploads/')),
                ('answer_key', models.CharField(default='', max_length=200)),
                ('marks_per_question', models.IntegerField(default=4)),
                ('number_of_question', models.IntegerField(default=5)),
            ],
        ),
    ]
