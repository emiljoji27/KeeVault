# Generated by Django 4.0.5 on 2022-07-31 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_passwordmodel_aes_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordmodel',
            name='img_url',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='passwordmodel',
            name='aes_key',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
