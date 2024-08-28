from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Yo'nalish")
    photo = models.ImageField(upload_to='jobs_photo/')

    def __str__(self):
        return self.name

class Jobs(models.Model):
    name = models.CharField(max_length=100, verbose_name="ish")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Yo'nalish")
    deman = models.TextField(verbose_name="Talab")
    salary = models.IntegerField(verbose_name="Maosh")
    # photo = models.ImageField(upload_to='jobs_photo/')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Muallif")
    views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addres = models.CharField(max_length=100, verbose_name="Manzil", null=True, blank=True)
    phone = models.CharField(max_length=14, verbose_name="Telefon raqam", null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    photo = models.ImageField(upload_to='profile/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"

class Comments(models.Model):
    author = models.CharField(max_length=100, verbose_name="Muallif")
    text = models.TextField(verbose_name="Izoh")
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

class CallBack(models.Model):
    author = models.CharField(max_length=100)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author
