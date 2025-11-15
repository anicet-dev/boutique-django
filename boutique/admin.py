from django.contrib import admin
from .models import Categorie, Produit, Order, OrderItem, Paiement


# ==========================
#  CATÉGORIE
# ==========================
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)


# ==========================
#  PRODUIT
# ==========================
@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix', 'stock', 'image_display')
    list_filter = ('categorie',)
    search_fields = ('nom', 'description')
    list_editable = ('prix', 'stock')

    def image_display(self, obj):
        """Affiche le nom de l’image dans l’admin."""
        if obj.image:
            return f"🖼️ {obj.image.url.split('/')[-1]}"
        return "Aucune"
    image_display.short_description = "Image"


# ==========================
#  ARTICLE DE COMMANDE (INLINE)
# ==========================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('produit', 'quantite', 'prix_unitaire', 'date_ajout')
    can_delete = False


# ==========================
#  COMMANDE
# ==========================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'telephone', 'mode_livraison', 'afficher_total', 'complete', 'date_commande')
    list_filter = ('complete', 'mode_livraison', 'date_commande')
    search_fields = ('nom', 'telephone', 'adresse')
    readonly_fields = ('date_commande',)
    inlines = [OrderItemInline]

    actions = ['marquer_commande_complete']

    def afficher_total(self, obj):
        """Affiche le total de la commande dans l’admin."""
        return f"{obj.get_total_commande()} FCFA"
    afficher_total.short_description = "Total"

    @admin.action(description="Marquer les commandes comme terminées")
    def marquer_commande_complete(self, request, queryset):
        updated = queryset.update(complete=True)
        self.message_user(request, f"{updated} commande(s) marquée(s) comme terminée(s).")


# ==========================
#  ARTICLE DE COMMANDE (DIRECT)
# ==========================
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'produit', 'quantite', 'prix_unitaire', 'date_ajout')
    list_filter = ('date_ajout',)
    search_fields = ('produit__nom', 'order__nom')


# ==========================
#  PAIEMENT
# ==========================
@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('order', 'montant', 'mode_paiement', 'date_paiement', 'statut')
    list_filter = ('mode_paiement', 'statut', 'date_paiement')
    search_fields = ('order__nom', 'mode_paiement')
