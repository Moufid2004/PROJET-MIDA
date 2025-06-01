from django.contrib import messages  # pour les notifications Django
from .base import Observer            # si Observer est défini dans base.py


class NotificationObserver(Observer):
    def update(self, event_name, **kwargs):
        request = kwargs.get('request')
        if not request:
            return

        # Produits
        if event_name == 'produit_ajoute':
            messages.success(request, f"✅ Produit ajouté avec succès.")
        
        elif event_name == 'produit_modifie':
            messages.info(request, f"✏️ Produit modifié avec succès.")
        
        elif event_name == 'produit_supprime':
            messages.warning(request, f"🗑️ Produit supprimé.")

        # Catégories
        elif event_name == 'categorie_ajoute':
            messages.success(request, f"📂 Catégorie ajoutée avec succès.")

        elif event_name == 'categorie_modifie':
            messages.info(request, f"✏️ Catégorie modifiée avec succès.")

        elif event_name == 'categorie_supprime':
            messages.warning(request, f"🗑️ Catégorie supprimée.")

        # Ventes
        elif event_name == 'vente_creee':
            messages.success(request, f"💰 Vente de enregistrée avec succès.")

        # Commandes
        elif event_name == 'commande_acceptee':
            messages.success(request, f"📦 Commande acceptée avec succès.")

        elif event_name == 'commande_refusee':
            messages.warning(request, f"❌ Commande refusée.")

        # Connexion
        elif event_name == 'utilisateur_connecte':
            messages.success(request, f"👋 Bienvenue!")
        
        if event_name == 'ferme_ajoute':
            messages.success(request, f"✅ ferme ajouté avec succès.")
        
        elif event_name == 'ferme_supprime':
            messages.warning(request, f"🗑️ ferme supprimé.")

        elif event_name == 'ferme_modifie':
            messages.info(request, f"✏️ ferme modifiée avec succès.")