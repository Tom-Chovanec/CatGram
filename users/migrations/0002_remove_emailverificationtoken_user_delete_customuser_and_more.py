# Generated by Django 5.2.1 on 2025-06-07 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailverificationtoken',
            name='user',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.DeleteModel(
            name='EmailVerificationToken',
        ),
    ]
