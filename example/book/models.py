from django.db import models


class Book(models.Model):
    TYPES = ((1, "Hardcover"), (2, "Softcover"))
    title = models.CharField(max_length=255)
    date_published = models.DateField(blank=True, null=True)
    type = models.IntegerField(choices=TYPES, default=1)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=1024)
    books = models.ManyToManyField(Book)
