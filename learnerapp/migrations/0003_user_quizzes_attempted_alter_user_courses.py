# Generated by Django 5.1.6 on 2025-02-24 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learnerapp', '0002_user_avg_score_user_score1_user_score2_user_score3_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='quizzes_attempted',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(default=None, related_name='student', to='learnerapp.course'),
        ),
    ]
