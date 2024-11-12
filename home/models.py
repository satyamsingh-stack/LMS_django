from django.db import models

# Create your models here.
class Items(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    membership_type=models.CharField(max_length=25)
    join_date=models.DateField()
    expiry_date=models.DateField()
    books_borrowed=models.IntegerField()
    max_books=models.IntegerField()
    overdue_fees=models.IntegerField()
    