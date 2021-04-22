# Generated by Django 3.2 on 2021-04-22 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carteiras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('saldo', models.DecimalField(decimal_places=2, default=0, max_digits=11)),
                ('centro_custo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='conta', to='carteiras.centrocusto')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.AddIndex(
            model_name='conta',
            index=models.Index(fields=['centro_custo_id', 'slug'], name='contas_cont_centro__3f1f45_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='conta',
            unique_together={('centro_custo_id', 'slug')},
        ),
    ]
