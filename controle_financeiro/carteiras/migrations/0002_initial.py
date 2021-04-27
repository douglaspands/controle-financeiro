# Generated by Django 3.2 on 2021-04-27 01:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carteiras', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='carteira',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='centrocusto',
            index=models.Index(fields=['carteira_id', 'id'], name='carteiras_c_carteir_d16da7_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='centrocusto',
            unique_together={('carteira_id', 'id')},
        ),
        migrations.AddIndex(
            model_name='carteira',
            index=models.Index(fields=['usuario_id', 'id'], name='carteiras_c_usuario_39eda9_idx'),
        ),
        migrations.AddIndex(
            model_name='carteira',
            index=models.Index(fields=['usuario_id', 'slug'], name='carteiras_c_usuario_771203_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='carteira',
            unique_together={('usuario_id', 'slug'), ('usuario_id', 'id')},
        ),
    ]
