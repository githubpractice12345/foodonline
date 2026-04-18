from django.db import models
from accounts.models import User
from menu.models import FoodItem
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #outdated
    # def __unicode__(self):
    #     return self.user

    #self.user is a User object not string.So convert to str.
    def __str__(self):
        return str(self.user)

    # def __str__(self):
    #     return f"{self.user} - {self.fooditem} ({self.quantity})"

class Tax(models.Model):
    tax_type = models.CharField(max_length=20, unique=True)
    tax_percentage = models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Tax Percentage(%)')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'tax'

    def __str__(self):
        return self.tax_type