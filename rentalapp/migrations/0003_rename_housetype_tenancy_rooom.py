# Generated by Django 5.0.2 on 2024-05-14 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapp', '0002_house_no_houses_room_alter_tenancy_housetype_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tenancy',
            old_name='housetype',
            new_name='rooom',
        ),
    ]