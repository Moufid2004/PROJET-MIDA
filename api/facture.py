from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

def generate_invoice(commande):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Infos
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, f"Facture Commande #{commande.pk}")
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Date : {commande.date_commande.strftime('%d/%m/%Y %H:%M')}")
    p.drawString(100, 750, f"Client : {commande.username}")
    p.drawString(100, 730, f"Email : {commande.useremail}")
    p.drawString(100, 710, f"Produit : {commande.produit}")
    p.drawString(100, 690, f"Quantité : {commande.quantite}")
    p.drawString(100, 670, f"Statut : {commande.status}")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
