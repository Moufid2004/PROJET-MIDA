# Generated by Django 5.2.1 on 2025-05-14 12:56

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Catégorie',
            fields=[
                ('idCategorie', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='inscription',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='pharmacies/photos/')),
                ('nom', models.CharField(blank=True, null=True)),
                ('adresse', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('proprietaire', models.CharField(blank=True, max_length=255, null=True)),
                ('numero_ordre', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ferme',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='fermes/photos/')),
                ('nom', models.CharField(blank=True, max_length=255, null=True)),
                ('adresse', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('password', models.CharField(max_length=255)),
                ('repassword', models.CharField(max_length=255)),
                ('proprietaire', models.CharField(blank=True, max_length=255, null=True)),
                ('numero_ordre', models.CharField(blank=True, max_length=100, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fermes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Produits',
            fields=[
                ('idProduit', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='produits/')),
                ('nom_produit', models.CharField(max_length=255)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=8)),
                ('description', models.TextField()),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.catégorie')),
                ('ferme', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ferme', to='backend.ferme')),
            ],
        ),
        migrations.CreateModel(
            name='Historique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_commande', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantite', models.IntegerField()),
                ('username', models.CharField(default='default_username', max_length=255)),
                ('useremail', models.EmailField(default='default@example.com', max_length=255)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], max_length=10)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.produits')),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_commande', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantite', models.PositiveIntegerField()),
                ('username', models.CharField(default='default_username', max_length=255)),
                ('useremail', models.EmailField(default='default@example.com', max_length=255)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.produits')),
            ],
        ),
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantite', models.IntegerField()),
                ('client', models.CharField(max_length=255)),
                ('date_commande', models.DateTimeField(default=django.utils.timezone.now)),
                ('produit', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='backend.produits')),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_facture', models.DateTimeField(default=django.utils.timezone.now)),
                ('montant_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.vente')),
            ],
        ),
    ]
