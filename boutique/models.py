from django.db import models
from django.conf import settings


# --- Catégories de produits ---
class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom


# --- Produits ---
class Produit(models.Model):
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name="produits"
    )
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nom


# --- Commandes ---
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    nom = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    adresse = models.TextField(blank=True, null=True)
    mode_livraison = models.CharField(
        max_length=50,
        choices=[
            ('livraison', 'Livraison à domicile'),
            ('retrait', 'Retrait sur place')
        ],
        default='livraison'
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    complete = models.BooleanField(default=False)
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande #{self.id} - {self.nom}"


# --- Éléments d’une commande ---
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantite} × {self.produit.nom}"


# --- Paiements ---
class Paiement(models.Model):
    MODE_CHOICES = [
        ('carte', 'Carte bancaire'),
        ('mobile_money', 'Mobile Money'),
        ('especes', 'Espèces'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('termine', 'Terminé'),
        ('echoue', 'Échoué'),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='paiements'
    )
    mode_paiement = models.CharField(max_length=20, choices=MODE_CHOICES)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )
    date_paiement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.id} - {self.order.nom} ({self.get_statut_display()})"
