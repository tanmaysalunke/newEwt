# Generated by Django 4.0.3 on 2022-03-25 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ewt', '0009_transactions'),
    ]

    operations = [
        migrations.CreateModel(
            name='uid_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('uid', models.JSONField()),
                ('category', models.CharField(max_length=20)),
                ('modified', models.BooleanField()),
            ],
        ),
    ]
