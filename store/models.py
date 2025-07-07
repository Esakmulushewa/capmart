from django.db import models

# Create your models here.
class Product(models.Model):
    category = models.CharField(max_length=100, default="")
    prod_name = models.CharField(max_length=100, default="")
    price = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True, default="")
    image = models.ImageField(null=True, blank=True, upload_to="images/")


    def __str__(self):
        return (self.prod_name + " || " + self.category)

 