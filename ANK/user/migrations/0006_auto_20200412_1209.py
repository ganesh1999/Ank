# Generated by Django 3.0.4 on 2020-04-12 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_result_updated_models'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='FailedNames',
            new_name='FailedinParticularSubject',
        ),
        migrations.RenameField(
            model_name='result',
            old_name='StudentInformation',
            new_name='FailedlistwithSubject',
        ),
        migrations.AddField(
            model_name='result',
            name='StudentRanking',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='SubjectResult',
            field=models.TextField(null=True),
        ),
    ]