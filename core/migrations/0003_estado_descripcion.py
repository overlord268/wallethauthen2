# Generated by Django 3.2.8 on 2021-12-15 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_transaccion_transaction_id_electrum'),
    ]

    operations = [
        migrations.AddField(
            model_name='estado',
            name='descripcion',
            field=models.CharField(default=None, max_length=150),
            preserve_default=False,
        ),
    ]
