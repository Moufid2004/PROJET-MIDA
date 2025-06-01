# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets,response,status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from api.models import *
from backend.models import *
from api.serializers import *
from django.http import HttpResponse
from api.facture import generate_invoice








class  ProduitsViewSet(viewsets.ModelViewSet):

    queryset = Produits.objects.all()
    serializer_class = ProduitsSerializer
    #permission_classes = [permissions.IsAdminUser]


class CatégorieViewSet(viewsets.ModelViewSet):

    queryset = Catégorie.objects.all()
    serializer_class = CatégorieSerializer
    #permission_classes = [permissions.IsAdminUser]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAdminUser]


class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    #permission_classes = [permissions.IsAdminUser]
    @action(detail=False, methods=['post'], url_path='create_commande')
    def create_commande(self, request, *args, **kwargs):
        data = request.data.copy()
        print(f"Received data: {data}")
        
        # Extraction de l'ID produit
        produit_url = data.get('produit')
        if produit_url:
            produit_id = produit_url.rstrip('/').split('/')[-1]
            print(f"Extracted product ID: {produit_id}")
            
            try:
                # MODIFICATION ICI: Utilisation de idProduit au lieu de id
                produit = Produits.objects.get(idProduit=produit_id)
                data['produit'] = produit.idProduit  # Stockez l'ID directement
            except Produits.DoesNotExist:
                return Response(
                    {"error": f"Product with ID {produit_id} not found"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "Product URL is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ensure required fields are present
        required_fields = ['quantite', 'username', 'useremail']
        for field in required_fields:
            if field not in data or not data[field]:
                return Response(
                    {"error": f"Missing required field: {field}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Create and validate the serializer
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the new Commande
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            print(f"Commande created successfully: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(f"Error creating commande: {str(e)}")
            return Response(
                {"error": f"Failed to create commande: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# @api_view(['POST'])
# def accepter_commande(request, pk):
#     try:
#         commande = Commande.objects.get(pk=pk)
#         commande.status = 'Accepted'
#         commande.save()
        
#         # Copier la commande dans l'historique
#         Historique.objects.create(
#             date_commande=commande.date_commande,
#             quantite=commande.quantite,
#             username=commande.username,
#             useremail=commande.useremail,
#             produit=commande.produit,
#             status='Accepted'
#         )
        
#         # Supprimer la commande originale
#         #commande.delete()

#         return Response({'status': 'Commande acceptée'}, status=status.HTTP_200_OK)
#     except Commande.DoesNotExist:
#         return Response({'error': 'Commande non trouvée'}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['POST'])
def accepter_commande(request, pk):
    try:
        commande = Commande.objects.get(pk=pk)
        commande.status = 'Accepted'
        commande.save()
        
        # Copier la commande dans l'historique
        Historique.objects.create(
            date_commande=commande.date_commande,
            quantite=commande.quantite,
            username=commande.username,
            useremail=commande.useremail,
            produit=commande.produit,
            status='Accepted'
        )
        
        # Générer la facture
        invoice_buffer = generate_invoice(commande)
        
        # Créer la réponse HTTP avec le fichier PDF
        response = HttpResponse(invoice_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="facture_{commande.pk}.pdf"'
        
        return response
        
    except Commande.DoesNotExist:
        return Response({'error': 'Commande non trouvée'}, status=status.HTTP_404_NOT_FOUND)








@api_view(['POST'])
def refuser_commande(request, pk):
    try:
        commande = Commande.objects.get(pk=pk)
        commande.status = 'Rejected'
        commande.save()
        
        # Copier la commande dans l'historique
        Historique.objects.create(
            date_commande=commande.date_commande,
            quantite=commande.quantite,
            username=commande.username,
            useremail=commande.useremail,
            produit=commande.produit,
            status='Rejected'
        )
        
        # Supprimer la commande originale
        #commande.delete()

        return Response({'status': 'Commande refusée'}, status=status.HTTP_200_OK)
    except Commande.DoesNotExist:
        return Response({'error': 'Commande non trouvée'}, status=status.HTTP_404_NOT_FOUND)


class FermeViewSet(viewsets.ModelViewSet):
    queryset = Ferme.objects.all()
    serializer_class = FermeSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email' 
    #permission_classes = [permissions.IsAdminUser]
