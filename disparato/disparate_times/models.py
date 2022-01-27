from tkinter import CASCADE
from django.db import models

# Create your models here.

class Word(models.Model):
    word = models.CharField(max_length=100)

class RelatedWord(models.Model):
    rel_word = models.CharField(max_length=100)
    rel_score = models.IntegerField()

    word = models.ForeignKey(Word, on_delete = models.CASCADE)

    def __str__(self):
        return f"{rel_word} has a score of {rel_score}"