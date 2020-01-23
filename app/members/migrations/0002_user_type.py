# Generated by Django 2.2.9 on 2020-01-23 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('N', 'NAVER'), ('F', 'FACEBOOK'), ('D', 'DEFAULT')], default='D', max_length=1),
        ),
    ]