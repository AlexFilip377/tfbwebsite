# Generated by Django 4.2.16 on 2024-10-29 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.RenameField(
            model_name='client',
            old_name='memmbership_number',
            new_name='membership_number',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='memmbership_price',
            new_name='membership_price',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='memmbership_type',
            new_name='membership_type',
        ),
    ]
