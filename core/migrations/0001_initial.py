# Generated by Django 3.1.2 on 2024-05-21 03:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('vigente', models.BooleanField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Compras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=50)),
                ('contacto', models.CharField(max_length=50)),
                ('fecha', models.DateField()),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.carrito')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
