# -*- coding: utf-8 -*-
from django.db import models

class Band(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    style = models.CharField(max_length=100, choices=(
        ('rock', 'Rock'),
        ('funk', 'Funk'),
        ('jazz', 'Jazz')
    ))
    agent = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Musician(models.Model):
    band = models.ForeignKey(Band, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, choices=(
        ('vocal', 'Vocal'),
        ('guitar', 'Guitar'),
        ('bass', 'Bass'),
        ('drums', 'Drums')
    ))


class Concert(models.Model):
    band = models.ForeignKey(Band, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=100)
    date = models.DateField()


class Album(models.Model):
    band = models.ForeignKey(Band, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    date = models.DateField()


class Interview(models.Model):
    band = models.ForeignKey(Band, on_delete=models.SET_NULL, null=True)
    media_name = models.CharField(max_length=100)
    date = models.DateField()
