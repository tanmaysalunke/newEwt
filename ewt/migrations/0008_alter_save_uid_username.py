# Generated by Django 4.0.3 on 2022-03-23 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ewt', '0007_alter_save_uid_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='save_uid',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]
