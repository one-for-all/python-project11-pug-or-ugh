from django.contrib.auth.models import User
from django.db import models


DOG_GENDER_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('u', 'Unknown'),
)

DOG_SIZE_CHOICES = (
    ('s', 'small'),
    ('m', 'medium'),
    ('l', 'large'),
    ('xl', 'extra large'),
    ('u', 'unknown'),
)


class Dog(models.Model):
    name = models.CharField(max_length=254)
    image_filename = models.CharField(max_length=254)
    breed = models.CharField(max_length=254, blank=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(choices=DOG_GENDER_CHOICES, max_length=1)
    size = models.CharField(choices=DOG_SIZE_CHOICES, max_length=2)

    def __str__(self):
        return self.name


STATUS_CHOICES = (
    ('l', 'liked'),
    ('d', 'disliked'),
)


class UserDog(models.Model):
    user = models.ForeignKey(User)
    dog = models.ForeignKey(Dog)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)

    def __str__(self):
        return "{} {} {}".format(self.user.username, self.get_status_display(),
                                 self.dog.name)


DOG_AGE_CHOICES = (
    ('b', 'baby'),
    ('y', 'young'),
    ('a', 'adult'),
    ('s', 'senior'),
)


class UserPref(models.Model):
    user = models.OneToOneField(User)
    age = models.CharField(max_length=254)
    gender = models.CharField(max_length=254)
    size = models.CharField(max_length=254)

    def __str__(self):
        return self.user.username
