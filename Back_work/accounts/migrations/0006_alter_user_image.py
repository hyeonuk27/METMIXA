# Generated by Django 3.2.3 on 2021-05-21 09:00

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(upload_to='profile_images/%Y/%m/%d/'),
        ),
    ]
