from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal
from .models import Produit, Order, OrderItem, Categorie, Paiement


# 🟢 PAGE D’ACCUEIL (produits regroupés par catégories)
def product_list(request):
    categories = Categorie.objects.prefetch_related('produits').all()
    return render(request, 'boutique/product_list.html', {'categories': categories})


# 🔵 Détail d’un produit
def product_detail(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    return render(request, 'boutique/product_detail.html', {'produit': produit})


# 🛒 Ajouter au panier
def add_to_cart(request, product_id):
    produit = get_object_or_404(Produit, id=product_id)
    qty = int(request.POST.get('quantity', 1))
    cart = request.session.get(settings.CART_SESSION_ID, {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += qty
    else:
        cart[str(product_id)] = {
            'name': produit.nom,
            'price': float(produit.prix),
            'quantity': qty,
            'image': produit.image.url if produit.image else '',
        }

    request.session[settings.CART_SESSION_ID] = cart
    messages.success(request, f"{produit.nom} ajouté au panier.")
    return redirect('boutique:cart')


# 🧺 Vue du panier
def cart_view(request):
    cart = request.session.get(settings.CART_SESSION_ID, {})
    items = []
    total = Decimal('0')

    for prod_id, info in cart.items():
        pid = int(prod_id)
        try:
            produit = Produit.objects.get(id=pid)
            prix = Decimal(str(info.get('price', produit.prix)))
        except Produit.DoesNotExist:
            produit = None
            prix = Decimal('0')

        quantite = int(info.get('quantity', 0))
        total_item = prix * quantite
        total += total_item
        items.append({
            'product_id': pid,
            'name': info.get('name'),
            'image': info.get('image'),
            'price': prix,
            'quantity': quantite,
            'total_item': total_item,
            'stock': produit.stock if produit else 0,
        })

    return render(request, 'boutique/cart.html', {'items': items, 'total': total})


# 🔁 Mise à jour panier (AJAX)
def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get(settings.CART_SESSION_ID, {})
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        qty = int(request.POST.get('quantity', 0))

        if not product_id:
            return JsonResponse({'error': 'product_id manquant'}, status=400)
        if str(product_id) not in cart:
            return JsonResponse({'error': 'produit non dans le panier'}, status=404)

        if action == 'set':
            cart[str(product_id)]['quantity'] = max(0, qty)
        elif action == 'inc':
            cart[str(product_id)]['quantity'] += 1
        elif action == 'dec':
            cart[str(product_id)]['quantity'] = max(0, cart[str(product_id)]['quantity'] - 1)

        if cart[str(product_id)]['quantity'] <= 0:
            del cart[str(product_id)]

        request.session[settings.CART_SESSION_ID] = cart

        total = sum(
            float(info['price']) * int(info['quantity'])
            for info in cart.values()
        )
        return JsonResponse({'total': total, 'cart': cart})

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


# ❌ Supprimer un produit du panier
def remove_from_cart(request, product_id):
    cart = request.session.get(settings.CART_SESSION_ID, {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session[settings.CART_SESSION_ID] = cart
        messages.info(request, "Produit retiré du panier.")
    return redirect('boutique:cart')


# 🚚 Page de livraison (checkout)
def checkout(request):
    cart = request.session.get(settings.CART_SESSION_ID, {})
    if not cart:
        messages.error(request, "Votre panier est vide.")
        return redirect('boutique:product_list')

    total = sum(Decimal(str(info['price'])) * int(info['quantity']) for info in cart.values())

    if request.method == 'POST':
        nom = request.POST.get('nom', '')
        telephone = request.POST.get('telephone', '')
        adresse = request.POST.get('adresse', '')
        mode_livraison = request.POST.get('mode_livraison', 'domicile')

        order = Order.objects.create(
            nom=nom,
            telephone=telephone,
            adresse=adresse,
            mode_livraison=mode_livraison,
            total=total,
            complete=False
        )

        for pid, info in cart.items():
            produit = Produit.objects.filter(id=int(pid)).first()
            OrderItem.objects.create(
                order=order,
                produit=produit,
                quantite=int(info['quantity']),
                prix_unitaire=Decimal(str(info['price']))
            )

        request.session['current_order_id'] = order.id
        return redirect('boutique:payment')

    return render(request, 'boutique/checkout.html', {'total': total})


# 💰 Paiement Mobile Money (simulation)
def payment_view(request):
    order_id = request.session.get('current_order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        moyen = request.POST.get('moyen', 'mobile_money')
        numero = request.POST.get('phone')

        Paiement.objects.create(
            order=order,
            mode_paiement=moyen,
            montant=order.total,
            statut='termine'
        )

        order.complete = True
        order.save()

        request.session[settings.CART_SESSION_ID] = {}

        messages.success(request, f"Paiement Mobile Money réussi pour {order.total} FCFA.")
        return redirect('boutique:order_success')

    return render(request, 'boutique/payment.html', {
        'order': order
    })


# ✅ Page de succès de commande
def order_success(request):
    return render(request, 'boutique/order_success.html')


# 📞 Page de contact
def contact(request):
    return render(request, 'boutique/contact.html')

def category_products(request, category_name):
    categorie = get_object_or_404(Categorie, nom__iexact=category_name)
    produits = categorie.produits.all()
    return render(request, 'boutique/category_products.html', {
        'category_name': categorie.nom,
        'produits': produits
    })


def ajouter_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    quantite = int(request.POST.get('quantite', 1))

    # On calcule le total pour cet article
    prix_total = produit.prix * quantite

    # Si tu as un modèle Order (panier ou commande)
    order, created = Order.objects.get_or_create(
        utilisateur=request.user,
        statut='en_cours'
    )

    # Crée ou met à jour un article
    item, created = OrderItem.objects.get_or_create(
        order=order,
        produit=produit,
        defaults={'quantite': quantite, 'prix': prix_total}
    )
    if not created:
        item.quantite += quantite
        item.prix = item.quantite * produit.prix
        item.save()

    return redirect('panier')
