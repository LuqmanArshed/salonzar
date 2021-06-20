# Generated by Django 3.1.4 on 2021-06-20 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salons', '0018_auto_20210620_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='type',
            field=models.CharField(blank=True, choices=[('shop', 'shop'), ('home', 'home')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(blank=True, choices=[('inprogress', 'inprogress'), ('pending', 'pending'), ('complete', 'complete')], max_length=200, null=True),
        ),
    ]