# Generated by Django 3.2 on 2021-06-12 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_alter_machine_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='fileName',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
