# Generated by Django 4.0.3 on 2022-03-18 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ewt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='category',
            field=models.CharField(choices=[('Manufacturer', 'Manufacturer'), ('Refurbisher', 'Refurbisher'), ('Recycler', 'Recycler')], default='Manufacturer', max_length=50),
        ),
    ]