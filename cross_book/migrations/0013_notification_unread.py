# Generated by Django 3.1.3 on 2021-04-25 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cross_book', '0012_auto_20210422_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='unread',
            field=models.BooleanField(default=True),
        ),
    ]