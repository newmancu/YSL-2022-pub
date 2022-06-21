# Generated by Django 4.0.3 on 2022-06-21 14:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShopUnitHistory',
            fields=[
                ('row_pk', models.BigAutoField(primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4)),
                ('name', models.CharField(max_length=256)),
                ('date', models.DateTimeField()),
                ('price', models.BigIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('parent_id', models.UUIDField(blank=True, null=True)),
                ('_type', models.CharField(choices=[('OFFER', 'OFFER'), ('CATEGORY', 'CATEGORY')], max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='ShopUnitBase',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('date', models.DateTimeField()),
                ('price', models.BigIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('_type', models.CharField(choices=[('OFFER', 'OFFER'), ('CATEGORY', 'CATEGORY')], max_length=16)),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='back_api.shopunitbase')),
            ],
        ),
    ]
