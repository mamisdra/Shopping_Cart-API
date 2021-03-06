from django.contrib.auth.models import User
from django.db import models

#Mes produits : Un ID, nom, prix et une image pour l'affichage
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return (self.name)

#Mon panier: User et Total
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return "{} : Total is {}€".format(self.user, self.total)

#Mes Entrées : Un produit, sa quantité et le panier auquel elle est liée
class Entry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "User: {} Item : {} quantity: {}".format(self.cart.user, self.product.name, self.quantity)
