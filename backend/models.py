from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Ferme
class Ferme(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fermes', default=1)
    id = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to='fermes/photos/', blank=True, null=True)
    nom = models.CharField(max_length=255, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255)
    repassword = models.CharField(max_length=255)
    proprietaire = models.CharField(max_length=255, blank=True, null=True)
    numero_ordre = models.CharField(max_length=100, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

class Catégorie(models.Model):
    idCategorie = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

class inscription(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to='fermes/photos/', blank=True, null=True)
    nom = models.CharField(blank=True, null=True,max_length=255)
    adresse = models.CharField(max_length=255,blank=True, null=True)  
    email = models.EmailField(blank=True, null=True)
    proprietaire = models.CharField(max_length=255,blank=True, null=True)
    numero_ordre = models.CharField(max_length=100,blank=True, null=True)
    

    def __str__(self):
        return self.nom

class Produits(models.Model):
    idProduit = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='produits/', null=False)
    nom_produit = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    categorie = models.ForeignKey(Catégorie, on_delete=models.CASCADE)
    ferme = models.ForeignKey(Ferme, on_delete=models.CASCADE, related_name='ferme', default=1)

    def __str__(self):
        return self.nom_produit

class Commande(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    id = models.AutoField(primary_key=True)
    date_commande = models.DateTimeField(default=timezone.now)
    quantite = models.PositiveIntegerField()
    username = models.CharField(max_length=255, default='default_username')
    useremail = models.EmailField(max_length=255, default='default@example.com')
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return str(self.id)

class Vente(models.Model):
    id = models.AutoField(primary_key=True)
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE, default=1)
    quantite = models.IntegerField()
    client = models.CharField(max_length=255)
    date_commande = models.DateTimeField(default=timezone.now)

class Historique(models.Model):
     date_commande = models.DateTimeField(default=timezone.now)
     quantite = models.IntegerField()
     username =  models.CharField(max_length=255, default='default_username')
     useremail = models.EmailField(max_length=255,default='default@example.com') 
     produit = models.ForeignKey(Produits, on_delete=models.CASCADE)
     status = models.CharField(max_length=10, choices=Commande.STATUS_CHOICES)

class Facture(models.Model):
    vente = models.OneToOneField(Vente, on_delete=models.CASCADE)
    date_facture = models.DateTimeField(default=timezone.now)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Facture {self.id} pour Vente {self.vente.id}'
