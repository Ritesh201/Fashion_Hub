# Generated by Django 3.0.5 on 2021-09-03 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20210903_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='serial_no',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Category'),
        ),
    ]
