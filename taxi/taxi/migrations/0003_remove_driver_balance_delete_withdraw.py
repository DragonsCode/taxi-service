# Generated by Django 5.0.2 on 2024-03-02 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0002_remove_client_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='balance',
        ),
        migrations.DeleteModel(
            name='Withdraw',
        ),
    ]
