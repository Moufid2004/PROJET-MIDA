from django.shortcuts import redirect, render, get_object_or_404
from backend.models import Catégorie,Produits,Ferme,Commande,Facture
from .forms import *
from django.core.mail import EmailMessage
from django.db.models import Q
from .models import Ferme
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.utils import timezone
from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from api.views import*
from django.contrib import messages  # Pour le système de messages de Django
from .notifications import NotificationObserver  # Votre classe Observer personnalisée


def notify(request, event_name, **kwargs):
    """Helper function for notifications"""
    NotificationObserver().update(event_name, request=request, **kwargs)

def handle_form(request, form_class, template, redirect_url, success_event=None, instance=None):
    """Generic form handling function"""
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save()
            if success_event:
                notify(request, success_event, **{success_event.split('_')[0]: obj})
            return redirect(redirect_url)
    else:
        form = form_class(instance=instance)
    
    return render(request, template, {'form': form, 'obj': instance})


def  Accueil(request):
    return render (request,'accueil.html')


@login_required
def  Logo(request):
    return render (request,'logo.html')

@login_required
def Dashboard(request):
    return render (request,'dashboard.html')

@login_required
def Commandes(request):
    commandes = Commande.objects.all()
    context = {
        'commandes': commandes
    }
    return render(request, 'commande.html', context)

@login_required
def  HistoriqueCommande(request):
    historiques = Historique.objects.all()
    return render(request, 'historique.html', {'historiques': historiques})


@login_required  
def modifyProduit(request,id):
     #récuperation des données de la base de donnée
    product = Produits.objects.get(idProduit=id)
  
   
    if request.method =='POST': 
        form = ProduitsForm(request.POST, instance=product)
        if form.is_valid():
            product =  form.save()
        NotificationObserver().update('produit_modifie', request=request)
        return redirect('liste_produits')
    else :
        print("let's modify")
        form = ProduitsForm(instance=product)
        print(form)
    return render (request, 'formulaire_produit.html',{'form':form, 'produits': product}) 

@login_required
def Creer_vente(request):
    if request.method == 'POST':
        form = VenteForm(request.POST, request.FILES)
        
        if form.is_valid():
            vente = form.save()

            # Calcul du montant total 
            montant_total = vente.produit.prix * vente.quantite 

            # Création de la facture
            facture = Facture.objects.create(vente=vente, montant_total=montant_total)
            
            NotificationObserver().update('vente_creee', request=request)

            return redirect('liste_ventes')
    else:
        form = VenteForm()

    return render(request, 'vente.html', {'form': form})

@login_required
def liste_ventes(request):
    vente = Vente.objects.all()
    return render(request, 'listeVente.html', {'ventes': vente})


def voir_facture(request, id):
    facture = get_object_or_404(Facture, id=id)
    return render(request, 'facture.html', {'facture': facture})


@login_required
def saveCatégorie(request):
    if request.method =='POST':
        form = CatégorieForm(request.POST)

        cat1 = form.save()
        NotificationObserver().update('categorie_ajoute', request=request)
        return redirect('view')
    
    else :
        form = CatégorieForm()

    return render (request, 'page.html',{'form':form}) 

@login_required
def view(request):
    categories = Catégorie.objects.all()
    return render(request, 'view.html', {'categories': categories})


@login_required
def ModifyCategorie(request,id):
     #récuperation des données de la base de donnée
    category = Catégorie.objects.get(idCategorie=id)
    form = CatégorieForm(instance=category)
    if request.method =='POST': 
        form = CatégorieForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            # Rediriger vers une page de succès ou de liste des catégories
        NotificationObserver().update('categorie_modifie', request=request)

        return redirect('view')
        
    return render (request, 'page.html',{'form':form, 'Categorie':Catégorie}) 


@login_required
def deleteCategorie(request,id):
     #récuperation des données de la base de donnée
    category = Catégorie.objects.get(idCategorie=id)
    category.delete()
    NotificationObserver().update('categorie_supprime', request=request)

    return redirect('view')
        


@login_required
def ajouter_produit(request):
    print("hello")
    if request.method =='POST':
        form = ProduitsForm(request.POST,request.FILES)
        
        if form.is_valid():
            img = form.cleaned_data.get("image")
            form.save()
            NotificationObserver().update('produit_ajoute', request=request)
            return redirect('liste_produits')
    
    else :
        form = ProduitsForm()

    return render (request, 'formulaire_produit.html',{'form':form}) 




@login_required
def liste_produits(request):
    produit = Produits.objects.all()
    return render(request, 'affichage.html', {'produits': produit})







@login_required
def deleteProduit(request,id):
     #récuperation des données de la base de donnée
    product = Produits.objects.get(idProduit=id)
    product.delete()
    NotificationObserver().update('produit_supprime', request=request)

    return redirect('liste_produits')
        



@login_required
@permission_required('ajouter_ferme', raise_exception=True)
def ajouter_ferme(request):
    error = False
    message = ""

    if request.method == "POST":
        photo = request.FILES.get('photo')
        nom = request.POST.get('nom')
        adresse = request.POST.get('adresse')
        email = request.POST.get('email')
        proprietaire = request.POST.get('proprietaire')
        numero_ordre = request.POST.get('numero_ordre')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        try:
            validate_email(email)
        except:
            error = True
            message = "Entrez un email valide svp!"

        if not error:
            if password != repassword:
                error = True
                message = "Les deux mots de passe ne correspondent pas!"

        if not error:
            user = User.objects.filter(email=email).first()
            if user:
                error = True
                message = f"Un utilisateur avec cet email {email} existe déjà!"

        if not error:
            print(nom)
            print(password)
            print(email)
            user = User.objects.create_user(
                email=email,
                password=password,
                username=nom,
                last_login=timezone.now()
            )
            user.save()
            print(user.id)
            ferme = Ferme.objects.create(
                nom=nom,
                adresse=adresse,
                email=email,
                password=password,
                proprietaire=proprietaire,
                numero_ordre=numero_ordre,
                photo=photo,
                user = user
            )
            print(ferme.photo)
            ferme.save()
           
            NotificationObserver().update('ferme_ajoute', request=request)

            return redirect('liste_ferme')

        context = {
            'error': error,
            'message': message
        }

        return render(request, 'formulaire_ferme.html', context)

    return render(request, 'formulaire_ferme.html', {})
    







@login_required
@permission_required('liste_ferme', raise_exception=True)
def liste_ferme(request):
    fermes = Ferme.objects.all()
    return render(request, 'ferme.html', {'fermes': fermes})


@login_required
@permission_required('modifyferme', raise_exception=True)
def modifyferme(request,id):
     #récuperation des données de la base de donnée
    ferm = Ferme.objects.get(id=id)

    if request.method =='POST': 
        form = FermeForm(request.POST, instance=ferm)
        if form.is_valid():
            ferm =  form.save()
        NotificationObserver().update('ferme_modifie', request=request)

        return redirect('liste_ferme')
    
    else :
        print("let's modify")
        form = FermeForm(instance=ferm)
        print(form)
    return render (request, 'formulaire_Ferme.html',{'form':form, 'fermes': ferm}) 


 


@login_required
@permission_required('deleteferme', raise_exception=True)
def deleteferme(request,id):
     #récuperation des données de la base de donnée
    ferm = Ferme.objects.get(id=id)
    ferm .delete()
    NotificationObserver().update('ferme_supprime', request=request)

    return redirect('liste_ferme')





@login_required
def recherche_produit(request):
    if request.method == 'POST':
        recherche = request.POST.get('recherche')
        produits = Produits.objects.filter(Medicament__icontains=recherche)
        categories = Catégorie.objects.filter(nom__icontains=recherche)
        return render(request, 'resultats_recherche.html', {'produits': produits, 'categories': categories})
    else:
        return render(request, 'formulaire_recherche.html')








#views authentification

def connexion(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        user = User.objects.filter(email=email).first()
        
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                NotificationObserver().update('utilisateur_connecte', request=request)  # Votre notification
                return redirect('Dashboard')
            else:
                messages.error(request, "Mot de passe incorrect")  # Feedback visuel
        else:
            messages.error(request, "Utilisateur inexistant")  # Feedback visuel
    
    return render(request, 'login.html', {})



def Inscription(request):
    if request.method == "POST":
        photo = request.FILES.get('photo')
        nom = request.POST.get('nom')
        adresse = request.POST.get('adresse')
        email = request.POST.get('email')
        proprietaire = request.POST.get('proprietaire')
        numero_ordre = request.POST.get('numero_ordre')

        # Vérification que tous les champs sont remplis
        if all([photo, nom, adresse, email, proprietaire, numero_ordre]):
            # Création de l'objet Pharmacie
            ferme = inscription.objects.create(
                nom=nom,
                adresse=adresse,
                email=email,
                proprietaire=proprietaire,
                numero_ordre=numero_ordre,
                photo=photo,
                
            )
            ferme.save()

            return redirect('Message')

        else:
            message = "Veuillez remplir tous les champs requis."
            context = {
                'error': True,
                'message': message
            }
            return render(request, 'register.html', context)

    return render(request, 'register.html', {})




def  Message(request):
    return render (request,'message.html')



@login_required
@permission_required('ferme.view_ferme', raise_exception=True)
def demande(request):
    fermes = inscription.objects.all()  # Récupère toutes les pharmacies inscrites
    return render(request, 'demande.html', {'fermes': fermes})




#def dashboard(request):
    return render(request, 'admin.html', {})

def sortie(request):
    logout(request)
    return redirect('Accueil')


def password_oublier(request):
    error = False
    success = False
    message = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            print("processing forgot password")
            html = """
                <p> Hello, merci de cliquer pour modifier votre email </p>
            """

            msg = EmailMessage(
                "Modification de mot de pass!",
                html,
                "bignuel@gmail.com",
                ["bignuel@gmail.com"],
            )

            msg.content_subtype = 'html'
            msg.send()
            
            message = "processing forgot password"
            success = True
        else:
            print("user does not exist")
            error = True
            message = "user does not exist"
    
    context = {
        'success': success,
        'error':error,
        'message':message
    }
    return render(request, "forgot_password.html", context)
    


def modifier_password(request):
    return render(request, "update_password.html", {})


