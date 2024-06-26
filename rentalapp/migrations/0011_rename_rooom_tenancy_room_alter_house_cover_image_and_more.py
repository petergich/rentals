# Generated by Django 4.2.3 on 2024-05-27 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapp', '0010_alter_house_cover_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tenancy',
            old_name='rooom',
            new_name='room',
        ),
        migrations.AlterField(
            model_name='house',
            name='cover_image',
            field=models.ImageField(upload_to='houses/'),
        ),
        migrations.AlterField(
            model_name='room',
            name='type',
            field=models.CharField(choices=[('single_room', 'Single Room'), ('bedsitter', 'Bedsitter'), ('one_bedroom', 'One Bedroom'), ('two_bedroom', 'Two Bedroom'), ('three_bedroom', 'Three Bedroom'), ('four_bedroom', 'Four Bedroom'), ('five_bedroom', 'Five Bedroom')], max_length=20),
        ),
    ]
