from django.conf import settings
from django.db import models

from multiselectfield import MultiSelectField

AGE_OPTION = (
    ('b', 'baby'),
    ('y', 'young'),
    ('a', 'adult'),
    ('s', 'senior'),
)

GENDER_OPTION = (
    ('m', 'male'),
    ('f', 'female'),
    ('u', 'unknown'),
)

SIZE_OPTION = (
    ('s', 'small'),
    ('m', 'medium'),
    ('l', 'large'),
    ('xl', 'extra large'),
    ('u', 'unknown'),
)

STATUS_OPTION = (
    ('l', 'liked'),
    ('d', 'disliked'),
)

class Dog(models.Model):
    name = models.CharField(max_length=100)
    image_filename = models.TextField()
    breed = models.CharField(max_length=100, default='unknown')
    age = models.PositiveIntegerField()
    gender = MultiSelectField(max_length=1, choices=GENDER_OPTION, default='u')
    size = MultiSelectField(max_length=2, choices=SIZE_OPTION, default='u')

    def __str__(self):
        return self.name


class UserPref(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    age = MultiSelectField(choices=AGE_OPTION, max_choices=4, default='b,y,a,s')
    gender = MultiSelectField(choices=GENDER_OPTION, max_choices=3, default='m,f')
    size = MultiSelectField(choices=SIZE_OPTION, max_choices=5, default='s,m')

    def __str__(self):
        return self.user.username


class UserDog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = MultiSelectField(max_length=1, choices=STATUS_OPTION)

    def __str__(self):
        return self.dog.name

