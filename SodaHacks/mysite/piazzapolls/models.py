from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

class TextResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=400)
    def __str__(self):
        return self.choice_text

class DateResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_date = models.DateTimeField('datetime answer')
    def __str__(self):
        return self.choice_date

    def compare(self, otherDateResponse):
        if self.choice_date > otherDateResponse.choice_date:
            return True
        else:
            return False

class Information(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    first_date = models.DateField()
    last_CID = models.IntegerField()
    course_ID = models.CharField(max_length=200)
    keywords = models.TextField()
    def __str__(self):
        return '{} - {} - {} - {}'.format(str(first_date),str(last_CID),str(course_ID),str(keywords))

class Term(models.Model):
    word = models.CharField(max_length=200)
    information = models.ForeignKey(Information, on_delete=models.CASCADE)
    def __str__(self):
        return word
