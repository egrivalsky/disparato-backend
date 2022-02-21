from datetime import datetime
from tkinter import CASCADE
from django.db import models


# Create your models here.

class Word(models.Model):
    word = models.CharField(max_length=100)
    written = models.DateField(null=True)
    last_accessed = models.DateField(null=True)
    times_accessed = models.IntegerField(default=0)
    rel_word = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.word} accessed {self.times_accessed} since {self.written}" 
