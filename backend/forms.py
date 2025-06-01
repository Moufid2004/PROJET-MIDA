from django import forms
from django.forms import ModelForm, Textarea
from .models import *
from django.forms.fields import ImageField

class CatégorieForm(ModelForm):
    class Meta:
        model = Catégorie
        fields = "__all__"

class ProduitsForm(ModelForm):
    image = ImageField(
        required=False,
    )
    
    class Meta:
        model = Produits
        fields = "__all__"
        widgets = {
            "description": Textarea(attrs={"cols": 40, "rows": 5}),
        }
        help_texts = {
            "idProduit": ("Le champ ID doit être unique."),
        }
        error_messages = {
            "nom": {
                "max_length": ("Ce nom est trop long."),
            },
        }

class FermeForm(ModelForm):
    class Meta:
        model = Ferme
        fields = ['photo', 'nom', 'adresse', 'email', 'password', 'repassword', 'proprietaire']
        # licence_exploitation et attestation_professionnelle supprimés

class CommandeForm(ModelForm):
    class Meta:
        model = Commande
        fields = "__all__"

class VenteForm(ModelForm):
    class Meta:
        model = Vente
        fields = ['produit', 'quantite', 'client']
