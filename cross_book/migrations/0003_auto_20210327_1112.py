# Generated by Django 3.0.3 on 2021-03-27 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cross_book', '0002_item_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='state',
            field=models.IntegerField(choices=[(0, '選択してください'), (1, '未使用'), (2, '未使用に近い状態'), (3, '目立った傷や汚れなし'), (4, 'やや傷や汚れあり'), (5, '傷や汚れあり'), (6, '全体的に状態が悪い')], null=True, verbose_name='商品の状態'),
        ),
        migrations.AlterField(
            model_name='item',
            name='explanation',
            field=models.TextField(blank=True, max_length=3000, verbose_name='出品者からの一言'),
        ),
    ]
