# Generated by Django 2.2.5 on 2019-10-29 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0006_auto_20191029_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=15),
        ),
    ]