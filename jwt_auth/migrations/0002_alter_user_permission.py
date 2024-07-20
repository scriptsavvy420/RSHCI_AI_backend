# Generated by Django 5.0.4 on 2024-07-20 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='permission',
            field=models.CharField(choices=[('customer', 'Customer'), ('admin', 'Admin'), ('super', 'Super'), ('member', 'Member')], default='customer', max_length=50),
        ),
    ]
