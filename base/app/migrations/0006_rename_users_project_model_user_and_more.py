# Generated by Django 4.2.16 on 2024-10-23 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0005_alter_client_model_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project_model',
            old_name='users',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='client_model',
            name='client_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='client_model',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]