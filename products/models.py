from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    image=models.CharField(max_length=2552)
    more_info = models.TextField()
    price = models.IntegerField()
    category = models.ManyToManyField(Category, related_name='products')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name
