from decimal import Decimal
from django.conf import settings
from .models import Produit

class Panier:
    def __init__(self, request):
        self.session = request.session
        panier = self.session.get(settings.CART_SESSION_ID)
        if not panier:
            panier = self.session[settings.CART_SESSION_ID] = {}
        self.panier = panier

    def add(self, produit, quantite=1):
        produit_id = str(produit.id)
        if produit_id not in self.panier:
            self.panier[produit_id] = {'quantite': 0, 'prix': str(produit.prix), 'nom': produit.nom}
        self.panier[produit_id]['quantite'] += quantite
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.panier
        self.session.modified = True

    def remove(self, produit):
        produit_id = str(produit.id)
        if produit_id in self.panier:
            del self.panier[produit_id]
            self.save()

    def __iter__(self):
        for item in self.panier.values():
            item['total'] = float(item['quantite']) * float(item['prix'])
            yield item

    def get_total(self):
        return sum(float(item['prix']) * item['quantite'] for item in self.panier.values())

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
