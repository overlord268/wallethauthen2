# Generated by Django 3.2.8 on 2021-12-23 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('idEstado', models.BigAutoField(db_column='idEstado', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('idTransaccion', models.BigAutoField(db_column='idTransaccion', primary_key=True, serialize=False)),
                ('amount_hnl', models.FloatField()),
                ('amount_btc', models.FloatField()),
                ('wallet_address', models.CharField(max_length=255)),
                ('btc_hnl_change', models.FloatField()),
                ('transaction_id_todopago', models.CharField(max_length=255)),
                ('transaction_id_electrum', models.CharField(max_length=255)),
                ('fecha_hora', models.DateTimeField(auto_now_add=True)),
                ('estado', models.ForeignKey(db_column='idEstado', on_delete=django.db.models.deletion.DO_NOTHING, to='core.estado')),
            ],
        ),
    ]
