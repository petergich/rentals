# Generated by Django 5.0.2 on 2024-05-29 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapp', '0014_alter_room_floor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='type',
            new_name='htype',
        ),
    ]
