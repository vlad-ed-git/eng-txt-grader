# Generated by Django 3.0.3 on 2020-02-20 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0003_auto_20200220_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputtexts',
            name='input_txts',
            field=models.FileField(unique=True, upload_to='input_txts/'),
        ),
    ]
