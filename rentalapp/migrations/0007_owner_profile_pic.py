# Generated by Django 4.2.3 on 2024-05-27 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapp', '0006_alter_house_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='profile_pic',
            field=models.ImageField(default='files/owners/a.png', upload_to='files/owners/'),
        ),
    ]