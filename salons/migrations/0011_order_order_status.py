# Generated by Django 3.1.4 on 2021-05-22 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salons', '0010_auto_20210518_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('inprogress', 'inprogress'), ('complete', 'complete')], max_length=200, null=True),
        ),
    ]