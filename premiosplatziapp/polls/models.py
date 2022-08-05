from pyexpat import model
from secrets import choice
from statistics import mode
from django.db import models
from django.utils import timezone

import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def choice_set_sorted(self):
        # Can set .order_by('-votes') to reverse order
        return self.choice_set.all().order_by('-votes')
    
    def max_voted(self):
        # return the first more voted
        return self.choice_set_sorted().first()

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
