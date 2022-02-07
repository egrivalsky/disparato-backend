from datetime import datetime
from tkinter import CASCADE
from django.db import models


# Create your models here.

class Word(models.Model):
    word = models.CharField(max_length=100)
    rel_word = models.TextField(default="{\"word\": \"time\", \"score\": \"1000\"}")
    written = models.DateField(null=True)
    last_accessed = models.DateField(null=True)
    times_accessed = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.word} accessed {self.times_accessed} since {self.written}" 

# class RelatedWord(models.Model):
#     rel_word = models.CharField(max_length=100)
#     rel_score = models.IntegerField()

#     word = models.ForeignKey(Word, on_delete = models.CASCADE)

#     def __str__(self):
#         return f"{self.rel_word} has a score of {self.rel_score}"