# Generated by Django 3.1.2 on 2024-05-26 22:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0008_auto_20240524_1312'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoAceptado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_pedido', models.CharField(max_length=20)),
                ('nombre_cliente', models.CharField(max_length=100)),
                ('subtotal', models.IntegerField()),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='boleta',
            name='aceptado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='boleta',
            name='bodeguero',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
