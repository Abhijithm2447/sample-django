# Generated by Django 3.0.4 on 2020-04-04 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0004_usermembershipdb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminprofiledb',
            name='phone',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='doctorprofiledb',
            name='phone',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='gymexpertprofiledb',
            name='phone',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofiledb',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
