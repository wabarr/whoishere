# Generated by Django 4.2.1 on 2023-08-31 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whoishere', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='nickname',
            field=models.CharField(blank=True, help_text='a shorthand way to refer to the course', max_length=50, null=True),
        ),
    ]
